import sys
from argparse import ArgumentParser
from http.client import RemoteDisconnected
from time import sleep
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
import csv
import hashlib
import json
import progressbar

bar = progressbar.ProgressBar()
last_count = 0


def download_progress(count, blockSize, totalSize):
    global last_count, bar
    if count > last_count + 10000:
        bar.max_value = totalSize
        bar.update(count * blockSize)
        last_count = count


def flush_batch(batch, url):
    global bar
    bar.update(bar.value + len(batch))
    r = request.Request(
        url=url,
        data=json.dumps(batch).encode('utf-8'),
        headers={
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    request.urlopen(r, timeout=10).read()


if __name__ == '__main__':

    # Batch size to feed to solr
    BATCH_SIZE = 1000

    parser = ArgumentParser()
    parser.add_argument('--base_url', required=True)
    args = parser.parse_args()

    retry = True
    retries = 0

    # Try until solr container/index becomes available
    while retry:
        try:
            sys.stdout.write('Creating index "summaries"...')
            response = request.urlopen(urljoin(args.base_url, '/solr/admin/cores?action=CREATE&name=summaries'))
            retry = False
            sys.stdout.write('ok.')
        except HTTPError as e:
            sys.stdout.write('Index already exists, will exit...\n')
            retry = False
            exit(0)
        except (RemoteDisconnected, URLError):
            sys.stdout.write('Solr container not yet available, retrying in 5 seconds...\n')
            sleep(5)
            retries += 1

            if retries > 10:
                sys.stdout.write('Solr container never became available, giving up.')
                exit(1)

    # Download summarization data to fill index
    sys.stdout.write('\nDownloading summarization data...')
    bar.widgets = [
        'Download progress: ', progressbar.Bar(), ' ', progressbar.Counter()
    ]
    download_csv = request.urlretrieve(
        url='https://drive.switch.ch/index.php/s/YoyW9S8yml7wVhN/download?path=%2F&files=data_train.csv',
        filename='/tmp/data_train.csv',
        reporthook=download_progress
    )
    sys.stdout.write('done.\n')

    # Load data into index
    sys.stdout.write('Filling index...')

    with open('/tmp/data_train.csv', 'r') as f:
        reader = csv.DictReader(f)
        num_docs = sum(1 for _ in reader)
        f.seek(0)
        bar.max_value = num_docs + 1
        bar.widgets = [
            'Indexed Documents: ', progressbar.Bar(), ' ', progressbar.Counter()
        ]
        bar.update(0)

        batch = []

        for row in reader:
            hash = hashlib.md5(row.get('source').encode('utf-8')).hexdigest()
            batch.append(
                {'hash': hash,
                 'text': row.get('source'),
                 'summary': row.get('summary')}
            )

            if len(batch) > BATCH_SIZE:
                flush_batch(batch, urljoin(args.base_url, '/solr/summaries/update/json/docs?commit=true'))
                batch = []

        flush_batch(batch, urljoin(args.base_url, '/solr/summaries/update/json/docs?commit=true'))

    sys.stdout.write('done.\n')

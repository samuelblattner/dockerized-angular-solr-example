import re
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
import spacy
import dateparser

from scripts.common import download_summarization_file_if_not_exists
from .topic_model.infer_topic_model import predict_topic

DATA_PATH = '/tmp/data_train.csv'

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

    nlp = spacy.load('de_core_news_sm', disable=['parser', 'ner', 'textcat'])

    # Batch size to feed to solr
    BATCH_SIZE = 50

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
            # exit(0)
        except (RemoteDisconnected, URLError):
            sys.stdout.write('Solr container not yet available, retrying in 5 seconds...\n')
            sleep(5)
            retries += 1

            if retries > 10:
                sys.stdout.write('Solr container never became available, giving up.')
                exit(1)

    # Download summarization data to fill index
    sys.stdout.write('\nDownloading summarization data...\n')
    sys.stdout.flush()
    bar.widgets = [
        'Download progress: ', progressbar.Bar(), ' ', progressbar.Counter()
    ]

    download_summarization_file_if_not_exists(DATA_PATH)

    sys.stdout.write('done.\n')

    # Load data into index
    sys.stdout.write('Filling index...')
    sys.stdout.flush()

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
        batch_texts = []
        batch_summaries = []
        date_regex = r'(\d{1,2}\.\s?(\d{1,2}\.\s?|\s?(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember))(\s?\d{4}))'

        for r, row in enumerate(reader):

            text = row.get('source')
            batch_texts.append(text)
            summary = row.get('summary')
            batch_summaries.append(summary)

            parsed_dates = [dateparser.parse(d[0]) for d in re.findall(date_regex, text)]

            batch.append(
                {
                    'id': hashlib.md5('{}{}'.format(text, summary).encode('utf-8')).hexdigest(),

                    'topic': predict_topic(text, top_n=2),
                    'text': text,
                    'text_length': len(text.split(' ')),
                    'text_num_dates': len(parsed_dates),
                    'text_dates': [d.strftime('%Y-%m-%d') for d in parsed_dates],

                    'summary': summary,
                }
            )

            if len(batch) > BATCH_SIZE:

                text_tags_batch = list(nlp.pipe(batch_texts, disable=['parser', 'ner', 'textcat']))
                text_nouns_batch = [sum([1 for tag in tags if tag.pos_ == 'NOUN']) for tags in text_tags_batch]
                text_verbs_batch = [sum([1 for tag in tags if tag.pos_ in ('VERB', 'AUX')]) for tags in text_tags_batch]

                summary_tags_batch = list(nlp.pipe(batch_summaries, disable=['parser', 'ner', 'textcat']))
                summary_nouns_batch = [sum([1 for tag in tags if tag.pos_ == 'NOUN']) for tags in summary_tags_batch]
                summary_verbs_batch = [sum([1 for tag in tags if tag.pos_ in ('VERB', 'AUX')]) for tags in summary_tags_batch]

                for item, item['text_num_nouns'], item['text_num_verbs'] in zip(batch, text_nouns_batch, text_verbs_batch):
                   pass

                flush_batch(batch, urljoin(args.base_url, '/solr/summaries/update/json/docs?commit=true'))
                batch = []
                batch_texts = []
                batch_summaries = []

        flush_batch(batch, urljoin(args.base_url, '/solr/summaries/update/json/docs?commit=true'))

    sys.stdout.write('done.\n')

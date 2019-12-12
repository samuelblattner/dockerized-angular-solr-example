import csv
import json
import os
import sys
from typing import Iterator
from urllib import request

import progressbar

bar = progressbar.ProgressBar()
last_count = 0


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

def download_progress(count, blockSize, totalSize):
    global last_count, bar
    if count > last_count + 10000:
        bar.max_value = totalSize
        bar.update(count * blockSize)
        last_count = count


def download_summarization_file_if_not_exists(to_path: str):
    # Download summarization data to fill index
    sys.stdout.write('\nDownloading summarization data...\n')
    sys.stdout.flush()
    bar.widgets = [
        'Download progress: ', progressbar.Bar(), ' ', progressbar.Counter()
    ]
    if not os.path.isfile(to_path):
        download_csv = request.urlretrieve(
            url='https://drive.switch.ch/index.php/s/YoyW9S8yml7wVhN/download?path=%2F&files=data_train.csv',
            filename=to_path,
            reporthook=download_progress
        )

    sys.stdout.write('done.\n')


def get_summarization_iter(from_path: str, limit: int = 0) -> Iterator:

    def gen():
        i: int = 0
        with open(from_path, 'r', encoding='utf-8') as f:

            reader = csv.DictReader(f)

            for row in reader:
                if i > limit > 0:
                    return
                yield row.get('source'), row.get('summary')

                i += 1

    return gen()

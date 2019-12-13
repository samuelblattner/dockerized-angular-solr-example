from argparse import ArgumentParser
from http.client import RemoteDisconnected
from time import sleep
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
import csv
import dateparser
import hashlib
import progressbar
import re
import spacy
import sys

from scripts.common import download_summarization_file_if_not_exists, bar, flush_batch
from scripts.topic_model.infer_topic_model import predict_topic


# Location where the original/raw dataset should be stored.
RAW_DATASET_PATH = '/tmp/data_train.csv'

# Batch size / number of documents to feed to solr at once in every iteration
BATCH_SIZE = 50

# Name of the Solr core to be created
INDEX_NAME = 'summaries'

# Max number of retries to connect to solr container before giving up
MAX_SOLR_CONNECT_RETRIES = 10

DATE_REGEX = r'(\d{1,2}\.\s?(\d{1,2}\.\s?|\s?(Januar|Februar|März|April|Mai|' \
             r'Juni|Juli|August|September|Oktober|November|Dezember))(\s?\d{4}))'


if __name__ == '__main__':
    """
    Main entry point for automated index creation and indexing.
    """

    # CLI parser to read base url. Base url of solr backend should be provided here
    parser = ArgumentParser()
    parser.add_argument('--base_url', required=True)
    parser.add_argument('--max_docs', required=False, default=1000)
    args = parser.parse_args()

    # Load Spacy NLP tool to perform POS-Tagging later on...
    nlp = spacy.load('de_core_news_sm', disable=['parser', 'ner', 'textcat'])

    retry_required = True
    retries = 0

    # 1. Create Solr Index
    # ====================
    # Try until solr container/index becomes available
    # If the index already exists, we exit the script and do nothing
    while retry_required:
        try:
            sys.stdout.write('Creating index "{name}"...'.format(name=INDEX_NAME))
            response = request.urlopen(
                url=urljoin(
                    args.base_url,
                    '/solr/admin/cores?action=CREATE&name={name}'.format(
                        name=INDEX_NAME
                    )
                )
            )
            retry_required = False
            sys.stdout.write('ok.')
        except HTTPError as e:
            sys.stdout.write('Index already exists, will exit...\n')
            retry_required = False
            exit(0)
        except (RemoteDisconnected, URLError):
            sys.stdout.write('Solr container not yet available, retrying in 5 seconds...\n')
            sleep(5)
            retries += 1

            if retries > MAX_SOLR_CONNECT_RETRIES:
                sys.stdout.write('Solr container never became available, giving up.')
                exit(1)

    # 2. Download Raw Dataset
    # =======================
    download_summarization_file_if_not_exists(RAW_DATASET_PATH)

    # 3. Perform Preprocessing and index data
    # =======================================
    sys.stdout.write('Filling index...')
    sys.stdout.flush()

    with open(RAW_DATASET_PATH, 'r') as f:
        reader = csv.DictReader(f)

        # Consume generator to count docs, then reset to 0
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

        for r, row in enumerate(reader):

            if r >= int(args.max_docs):
                break

            text = row.get('source')
            batch_texts.append(text)
            summary = row.get('summary')
            batch_summaries.append(summary)

            parsed_dates = [dateparser.parse(d[0]) for d in re.findall(DATE_REGEX, text)]

            batch.append(
                {
                    'id': hashlib.md5('{}{}'.format(
                        text, summary
                    ).encode('utf-8')).hexdigest(),

                    'topic': predict_topic(text, top_n=2),
                    'text': text,
                    'text_length': len(text.split(' ')),
                    'text_num_dates': len(parsed_dates),
                    'text_dates': [d.strftime('%Y-%m-%d') for d in parsed_dates],

                    'summary': summary,
                }
            )

            if len(batch) > BATCH_SIZE:

                text_tags_batch = list(
                    nlp.pipe(batch_texts, disable=['parser', 'ner', 'textcat'])
                )
                text_nouns_batch = [
                    sum([1 for tag in tags if tag.pos_ == 'NOUN']) for tags in text_tags_batch]

                text_verbs_batch = [
                    sum([1 for tag in tags if tag.pos_ in ('VERB', 'AUX')]) for tags in text_tags_batch]

                for item, item['text_num_nouns'], item['text_num_verbs'] in zip(batch, text_nouns_batch, text_verbs_batch):
                   pass

                flush_batch(batch, urljoin(args.base_url, '/solr/summaries/update/json/docs?commit=true'))
                batch = []
                batch_texts = []
                batch_summaries = []

        flush_batch(batch, urljoin(args.base_url, '/solr/summaries/update/json/docs?commit=true'))

    sys.stdout.write('done.\n')

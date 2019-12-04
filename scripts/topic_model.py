import csv
import os
from urllib import request

import gensim

import nltk
import progressbar

bar = progressbar.ProgressBar()
last_count = 0

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()


def download_progress(count, blockSize, totalSize):
    global last_count, bar
    if count > last_count + 10000:
        bar.max_value = totalSize
        bar.update(count * blockSize)
        last_count = count


if not os.path.isfile('./summarizations.csv'):
    download_csv = request.urlretrieve(
        url='https://drive.switch.ch/index.php/s/YoyW9S8yml7wVhN/download?path=%2F&files=data_train.csv',
        filename='./summarizations.csv',
        reporthook=download_progress
    )

normalized_docs = []
stop_words = nltk.corpus.stopwords.words('german')

with open('./summarizations.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    i = 0
    for r, row in enumerate(reader):
        text = str(row.get('source').lower().strip())

        text_tokens = [token.strip() for token in tokenizer.tokenize(text)]
        lemm_tokens = [lemmatizer.lemmatize(token) for token in text_tokens if not token.isnumeric()]

        normalized = list(filter(lambda t: len(t) > 1 and t not in stop_words, lemm_tokens))
        if normalized:
            normalized_docs.append(normalized)

        i += 1

        print(i)
        if i > 1000:

            break


# Create common bigrams (occurence >= 20,
bigram = gensim.models.Phrases(normalized_docs, min_count=20, threshold=20, delimiter=b'__')
bigram_model = gensim.models.phrases.Phraser(bigram)
#
doc_bigrams = [bigram_model[doc] for doc in normalized_docs]
dictionary = gensim.corpora.Dictionary(doc_bigrams)

dictionary.filter_extremes(no_below=20, no_above=0.6)

bow_corpus = [dictionary.doc2bow(doc) for doc in doc_bigrams]

lsi_bow = gensim.models.LsiModel(bow_corpus, id2word=dictionary, num_topics=10, onepass=True, chunksize=1740, power_iters=1000)

for topic_id, topic in lsi_bow.print_topics(num_topics=10, num_words=20):
    print('Topic ', topic_id + 1)
    print(topic)
    print()
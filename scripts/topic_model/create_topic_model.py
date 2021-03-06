import numpy as np
import pandas
import pandas as pd
import pickle

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from scripts.common import download_summarization_file_if_not_exists, get_summarization_iter
from scripts.topic_model.utils import normalize_texts


DATA_PATH = './summarizations.csv'
N_DOCS = 200000
N_TOPICS = 20


download_summarization_file_if_not_exists(DATA_PATH)

cv = CountVectorizer(
    min_df=200,
    max_df=0.2,
    ngram_range=(1, 2),
    token_pattern=None,
    tokenizer=lambda doc: doc,
    preprocessor=lambda doc: doc
)

cv_features = cv.fit_transform(
    map(lambda text: normalize_texts(list(text))[0], filter(
        lambda row: row[0], get_summarization_iter(DATA_PATH, limit=N_DOCS)
    ))
)
vocab = np.array(cv.get_feature_names())

nmf_model = NMF(
    n_components=N_TOPICS,
    solver='cd',
    max_iter=1000,
    random_state=42,
    alpha=.1,
    l1_ratio=0.85
)

doc_topics = nmf_model.fit_transform(cv_features)

with open('./model/topic_model.pkl', 'wb') as f:
    pickle.dump(nmf_model, f)

with open('./model/vocab.pkl', 'wb') as f:
    pickle.dump(cv.vocabulary_, f)

topic_terms = nmf_model.components_
topic_key_term_idxs = np.argsort(-np.absolute(topic_terms), axis=1)[:, :20]
topic_keyterms = vocab[topic_key_term_idxs]
topics = [', '.join(topic) for topic in topic_keyterms]
pd.set_option('display.max_colwidth', -1)
topics_df = pd.DataFrame(topics, columns=['Terms per Topic'], index=['Topic' + str(t) for t in range(1, N_TOPICS + 1)])

topics_df.to_csv('./model/topics.csv')

pandas.options.display.float_format = '{:,.3f}'.format
dt_df = pandas.DataFrame(doc_topics, columns=['T' + str(i) for i in range(1, N_TOPICS + 1)])
pandas.options.display.float_format = '{:,.5f}'.format
pandas.set_option('display.max_colwidth', 200)

max_score_topics = dt_df.max(axis=0)
dominant_topics = max_score_topics.index
term_score = max_score_topics.values
document_numbers = [dt_df[dt_df[t] == max_score_topics.loc[t]].index[0] for t in dominant_topics]
all_texts = [summary for text, summary in get_summarization_iter(DATA_PATH, limit=N_DOCS)]

documents = [all_texts[i] for i in document_numbers]
result_df = pandas.DataFrame({
    'Dominant Topic': dominant_topics,
    'Max Score': term_score,
    'Text Idx': document_numbers,
    'Topic': topics_df['Terms per Topic'],
    'Summary': documents
})

result_df.to_csv('./model/best_fits.csv')

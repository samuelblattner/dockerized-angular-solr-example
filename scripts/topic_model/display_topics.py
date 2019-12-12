import pickle
from os.path import join, dirname

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer

with open(join(dirname(__file__), './model/topic_model.pkl'), 'rb') as f:
    topic_model: NMF = pickle.load(f)

with open(join(dirname(__file__), './model/vocab.pkl'), 'rb') as f:
    vocab = pickle.load(f)

cv = CountVectorizer(
    min_df=1,
    max_df=0.6,
    ngram_range=(1, 2),
    token_pattern=None,
    tokenizer=lambda doc: doc,
    preprocessor=lambda doc: doc,
    vocabulary=vocab
)

print(topic_model.components_)
print(topic_model.components_.shape)

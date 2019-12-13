from typing import List

import string
import nltk


nltk.download('stopwords')

tokenizer = nltk.tokenize.RegexpTokenizer(r'\s', gaps=True)
stemmer = nltk.stem.SnowballStemmer('german', True)
stop_words = nltk.corpus.stopwords.words('german') + ['dass', 'jedoch', ]


def normalize_texts(texts: List[str]) -> List[List[str]]:
    """
    Normalization of texts:
    - lower case
    - remove punctuation, heading and trailing spaces
    - use stems
    - tokenize
    :param texts: Texts to be normalized
    :type texts: List[str]
    :return: List of token lists
    :rtype List[List[str]]
    """

    normalized_texts: List[List[str]] = []

    for text in texts:

        tokens = [t.strip(string.punctuation).strip()
                  for t in tokenizer.tokenize(text.lower()) if t not in stop_words]

        stemmed_tokens = [stemmer.stem(t) for t in tokens if not t.isnumeric()]

        normalized = list(filter(lambda t: len(t) > 1, stemmed_tokens))

        if normalized:
            normalized_texts.append(normalized)

    return normalized_texts

import pickle
from os.path import dirname, join

import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer

from scripts.topic_model.utils import normalize_texts

TOPICS = (
    'Wissenschaft & Technik',
    'Fussball',
    'Bildung',
    'Familie',
    'Dynastien',
    'Verkehr',
    'Geografie',
    'Adel',
    'Schiffahrt',
    'Sport',
    'Botanik',
    'Geschichte',
    'Musik',
    'Film',
    'Könige',
    'Kirchen',
    'Politik',
    'Hockey',
    'Definitionen',
    'Deutschland',
)

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


def predict_topic(text: str, top_n=1) -> [str]:
    p = topic_model.transform(
        cv.fit_transform(
            normalize_texts([text])
        )
    )
    scores = np.argsort(p)[0]
    return [TOPICS[scores[-(n + 1)]] for n in range(top_n)]


if __name__ == '__main__':
    print(predict_topic(
        'Minghella war der Sohn italienisch-schottischer Eltern, die auf der Isle of Wight eine Fabrik für Eiscreme betrieben. Nach seinem Schulabschluss studierte er an der Universität Hull, wo er eine Zeit lang als Dozent tätig war. 1978 drehte er einen ersten Kurzfilm. Seit 1981 war er als Autor und Story Editor tätig. Er wurde mit Theaterstücken, Rundfunkhörspielen, der Fernsehserie ""Inspector Morse"" und vielen Drehbüchern für Film und Fernsehen bekannt. Er entwickelte die Drehbücher für die 1988 erfolgreich ausgestrahlte Fernsehserie The Storyteller von Muppets-Erfinder Jim Henson. Auch als Produzent war er erfolgreich, darunter für die Filme ""Der stille Amerikaner"", ""Die Dolmetscherin"" und ""Der Vorleser"", für den er 2008 posthum für den Oscar nominiert wurde. Gemeinsam mit seinem Freund und Kollegen Sydney Pollack gründete er die Produktionsfirma Mirage Enterprises. Der Regisseur Minghella galt als ein guter Schauspielerführer: Unter seiner Regie brachten es zahlreiche Darsteller zu Oscar-Nominierungen, zwei Schauspielerinnen erhielten die Auszeichnung als ""Beste Nebendarstellerin"": Juliette Binoche und Renée Zellweger . Gegen Ende seines Lebens kehrte Minghella zu seinen Anfängen im Radio und auf der Bühne zurück: 2006 wurde sein Hörspiel ""Eyes Down Looking"" mit Jude Law zu Ehren von Samuel Beckett auf BBC Radio 3 ausgestrahlt, ein Jahr zuvor hatte seine Inszenierung der Puccini-Oper Madame Butterfly in der English National Opera in London Premiere und wurde auch in der Nationaloper von Vilnius und in der Metropolitan Opera in New York gezeigt. Am Ende des Films ""Abbitte"" von Joe Wright hat er einen Kurzauftritt als Talkshow-Moderator neben Vanessa Redgrave. Seine letzte Arbeit als Drehbuchautor war das Skript für den Musical-Film ""Nine"" . Zu seinen letzten Regiearbeiten zählt der Pilotfilm zur Krimiserie ""Eine Detektivin für Botswana"" , den die BBC fünf Tage nach seinem Tod erstmals ausstrahlte. Minghella war mit der aus Hongkong stammenden Choreographin, Produzentin und Schauspielerin Carolyn Choa verheiratet. Der Ehe entstammen zwei Kinder, die in der Filmbranche tätig sind: Tochter Hannah Minghella in der Produktion und Sohn Max Minghella als Schauspieler . Die Tante Edana Minghella und der Onkel Dominic Minghella sind Drehbuchautoren. Minghella starb im Alter von 54 Jahren in einem Londoner Krankenhaus an inneren Blutungen infolge der Operation eines Tonsillenkarzinoms und eines Karzinoms im Nacken. 1984 erhielt Minghella den Londoner Kritikerpreis als meistversprechender junger Dramatiker, 1986 den Kritikerpreis für sein Stück ""Made in Bangkok"" als bestes Stück der Saison. 1997 erhielt er für ""Der englische Patient"" den Oscar in der Rubrik ""Beste Regie"", 1999 eine Oscar-Nominierung in der Kategorie ""Bestes adaptiertes Drehbuch"" für ""Der talentierte Mr. Ripley"", bei dem er auch Regie führte. 2001 wurde Minghella zum Commander of the British Empire ernannt. Von 2003 bis 2007 war er Präsident des British Film Institute. Seit 1997 trägt das Anthony Minghella Theatre auf der Isle of Wight seinen Namen.', top_n=3))
    print(predict_topic(
        'Mykonos (griechisch Μύκονος [ˈmikɔnɔs] (f. sg.)) ist eine Insel der Kykladen im Ägäischen Meer. Zusammen mit Delos, der unbewohnten Insel Rinia und einigen kleinen Eilanden bildet sie eine Gemeinde und zugleich den Regionalbezirk Mykonos (griechisch Περιφερειακή Ενότητα Μυκόνου), der zwei Abgeordnete in den Regionalrat der Region Südliche Ägäis entsendet. Die Insel hat eine Fläche von 86,125 km²[2] und 10.134 Einwohner.[1] Die Hauptstadt der Insel – die Chora – heißt ebenfalls Mykonos. Die Insel zählt zu den populärsten griechischen Inseln mit Massentourismus'))

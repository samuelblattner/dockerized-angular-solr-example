Daten und Feature-Engineering
=============================
Der Index wird mit Daten der «German Text Summarization Challenge 2019» aufgebaut (siehe: https://www.swisstext.org/swisstext.org/2019/shared-task/german-text-summarization-challenge.html).
Der Datensatz umfasst 100'000 Texteinträge mit jeweils zugehöriger, manuell redigierter Zusammenfassung.
Der Datensatz hat entsprechend eine sehr einfache Struktur:

.. csv-table:: data_train.csv
    :file: ../tables/train.csv
    :widths: 70,30
    :header-rows: 1
    :encoding: utf-8


Wie vorgängig erwähnt, soll das Preprocessing, also die Normalisierung, das Feature Engineering und die Indexierung
der Dokumente automatisch und reproduzierbar ablaufen.
Zu diesem Zweck soll folgende Grafik einen Überblick über das Preprocessing bzw. den Datenfluss geben:

.. figure:: ../images/data.png

    Datenfluss von Rohdokument bis Index.
    Neben den bereits vorhandenen Feldern *source* und *summary* werden weitere Felder über Feature-Engineering indexiert.


Nebst den im Datensatz vorhandenen Feldern *source* sowie *summary* (Volltext und Zusammenfassung), werden diverese weitere Felder
via Feature-Engineering indexiert, um den Anforderungen des Auftraggebers zu genügen. Die Einzelnen Prozesse sind nachfolgend
im Detail beschrieben.

Einstieg in den automatischen Ablauf bildet das Modul *scripts/__main__.py*.



Datumsangaben
-------------
Die Daten enthalten ausschliesslich Texte in deutscher Sprache.
Damit können Datumsangaben in einfacher Weise gefunden werden.
Um die Formate *dd.mm.yyyy* sowie *dd.M.yyyy* in den Texten zu finden wird folgende Regular Expression verwendet:

.. code-block::

    (\d{1,2}\.\s?(\d{1,2}\.\s?|\s?(Januar|Februar|März|April|Mai|Juni|Juli|
    August|September|Oktober|November|Dezember))(\s?\d{4}))

Davon wird einerseits die Anzahl pro Text im Feld *text_num_dates* und andererseits die effektiven Daten im Feld *text_dates* indexiert.
Für das Parsen von Daten in Textformat wird die Bibliothek «dateparser» verwendet.


Part-Of-Speech Tagging
----------------------
Mit der NLP-Bibliothek «Spacy» können Texte mit wenig Aufwand analysiert werden.
U.a. steht auch die Funktion «Part-Of-Speach» Taggin zur Verfügung, wo die Wörter der Texte mit ihren jeweiligen Wortarten annotiert werden:

.. literalinclude:: ../../../scripts/__main__.py
    :lines: 136
    :linenos:

Zur schnelleren Verarbeitung werden die Texte batch-weise Spacy übergeben.
Ausserdem werden die Bestandteile *parser* (Abhängigkeiten von Satzteilen), *ner* (Named Entity Recognition, erkennen von referenzierten Objekten, z.B. Orte, Menschen, etc.) sowie
*textcat* (Textkategorisierung) ausgeschaltet, um den Prozessor von nicht benötigten Berechnungen zu entlasten.
Für die Textkategorisierung wird ein eigenes Modell trainiert (siehe weiter unten).


Topic Modeling
--------------
Der Datensatz enthält Texte aus verschiedenen Sachgebieten.
Die Themen sind jedoch nicht im Datensatz vorhanden und müssen erzeugt werden.
Dafür wird ein «Topic Model» auf Basis der Non-negative Matrix Factorization Methode trainiert.

.. code-block:: python

    cv = CountVectorizer(
        min_df=20,
        max_df=0.6,
        ngram_range=(1, 2),
        token_pattern=None,
        tokenizer=lambda doc: doc,
        preprocessor=lambda doc: doc
    )

    nmf_model = NMF(
        n_components=N_TOPICS,
        solver='cd',
        max_iter=1000,
        random_state=42,
        alpha=.1,
        l1_ratio=0.85
    )

    cv_features = cv.fit_transform(
    map(lambda text: normalize_texts(list(text))[0], filter(
        lambda row: row[0], get_summarization_iter(DATA_PATH, limit=N_DOCS)
    )))

    doc_topics = nmf_model.fit_transform(cv_features)


Das unsupervised learning gruppiert Wörter für 20 Themen wie folgt:

.. csv-table:: Topics
    :file: ../tables/topics.csv
    :widths: 10,20,70
    :header-rows: 1
    :encoding: utf-8

Viele der Themen sind nicht eindeutig

Daten und Feature-Engineering
=============================
Der Index wird mit Daten der «German Text Summarization Challenge 2019» aufgebaut (siehe: https://www.swisstext.org/swisstext.org/2019/shared-task/german-text-summarization-challenge.html).
Der Datensatz umfasst 100'000 Texteinträge mit jeweils zugehöriger, manuell redigierter Zusammenfassung.
Beim Starten des *Python-Scripts* Containers wird der Datensatz automatisch heruntergeladen und indexiert.
Nebst den im Datensatz vorhandenen Feldern *source* sowie *summary* (Volltext und Zusammenfassung), werden diverese weitere Felder
via Feature-Engineering indexiert, um den Anforderungen des Auftraggebers zu genügen.
Im Folgenden wird der Datenfluss schematisch dargestellt:

.. figure:: ../images/data.png

    Datenfluss von Rohdokument bis Index.
    Neben den bereits vorhandenen Feldern *source* und *summary* werden weitere Felder über Feature-Engineering indexiert.


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
U.a. steht auch die Funktion «Part-Of-Speach» Taggin zur Verfügung, wo die Wörter der Texte mit ihren jeweiligen Wortarten annotiert werden.


Topic Modeling
--------------
Der Datensatz enthält Texte aus verschiedenen Sachgebieten.
Die Themen sind jedoch nicht im Datensatz vorhanden und müssen erzeugt werden.
Dafür wird ein «Topic Model» auf Basis der Non-negative Matrix Factorization Methode trainiert.
Das unsupervised learning gruppiert Wörter für 20 Themen wie folgt:

.. csv-table:: Topics
    :file: ../tables/topics.csv
    :widths: 10,20,70
    :header-rows: 1
    :encoding: utf-8

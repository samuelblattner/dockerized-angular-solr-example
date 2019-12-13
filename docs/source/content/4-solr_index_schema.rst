Solr Index
==========

Der Index wird automatisch mit Apache Solr erzeugt und befüllt.
Dieser Abschnitt beschreibt einerseits das Schema, das den Index beschreibt und andererseits den automatischen Ablauf.

Schema
------
Die Erzeugung eines Schemas für den Index wird zunächst Solr überlassen.
Solr wählt die Feldtypen für ein paar testweise indexierte Dokumente automatisch und widerspiegelt sie in einem «Managed Schema».
Dies bietet eine ideale Ausgangslage, um das Schema anschliessend zu präzisieren und den Umfang zu reduzieren.
Dazu wird die Datei «managed_schema.xml» kopiert und in «schema.xml» umbenannt.
Zahlreiche nicht benötigte Felder und Feldtypen werden entfernt.
Das fertige Schema ist wie folgt aufgebaut:

.. literalinclude:: ../../../solr/conf/schema.xml
    :language: xml
    :linenos:

Übrig bleiben somit die Datentypen *int*, *long*, *string*, *date* und *text* (Zeilen 6 - 10).
Der Feldtyp «text_general» ist als einziger komplex und verwendet sowohl während der Indexierung als auch bei Abfragen
einen *StandardTokenizer*, um die eingelesenen Zeichenfolge in einzelne Wörter aufzuteilen sowie einen *LowerCaseFilter*, um ebendiese
in Kleinschreibweise umzuwandeln.
Mit dem *StopFilter* werden Stoppwörter aus dem deutschen Vokabular herausgefiltert.
Damit wird Anforderung Nr. 3 entsprochen (Zeilen 12 - 19).


Automatische Erzeugung
----------------------
Sobald der Solr-Container verfügbar ist, wird versucht, den Index *summaries* zu erzeugen.
Existiert er bereits, wird der Prozess abgebrochen.

.. literalinclude:: ../../../scripts/__main__.py
   :language: python
   :lines: 57-72
   :linenos:

Anschliessend werden die Dokumente stapelweise indexiert:

.. literalinclude:: ../../../scripts/__main__.py
   :language: python
   :lines: 120-150
   :linenos:

Zur eindeutigen Identifikation wird die id mittels Hash basierend auf dem Inhalt der Dokumente indexiert.

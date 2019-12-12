Solr Index
==========

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
The core is automatically created when the docker container is initialized.
A python script *create_index.py* automatically tries to create the core and exits without error if the core already exists.

.. literalinclude:: ../../../scripts/index/create_index.py
   :language: python
   :lines: 52-69
   :linenos:


Auftrag & Lösungsvorschlag
==========================
Dieser Bericht beschreibt die Anforderungen, den Lösungsvorschlag sowie den Arbeitsprozess für den Arbeitsauftrag im Modul Information Retrieval an der FFHS.
Der Auftrag besteht darin, einen Index inkl. GUI mit Apache Solr anhand von einer Liste von Anforderungen aufzubauen und zu befüllen.
In diesem Abschnitt wird zunächst der verwendete Datensatz kurz vorgestellt.
Anschliessend werden die Anforderungen beschrieben und analysiert sowie die Architektur der vorgeschlagenen Lösung beschrieben.

Swiss Text 2019 Summarization Challenge Datensatz
-------------------------------------------------
Als Grundlage für den Arbeitsauftrag dient der Datensatz der Swiss Text 2019 (https://www.swisstext.org/swisstext.org/2019/shared-task/german-text-summarization-challenge.html).
Der Datensatz wurde im Rahmen eines Wettbewerbs zur Verfügung gestellt und umfasst 100'000 Texte mit ihren jeweiligen Goldstandardzusammenfassungen.
Die Texte sind aus unterschiedlichen Themengebieten zusammengetragen.

Anforderungen
-------------
Die Anforderungen für den Index hat der Auftraggeber wie folgt definiert:

1. Ich möchte jeden Text auf eine zu definierende Anzahl Wörter zusammenfassen können
2. Ich möchte Texte basierend auf den Inhalt durchsuchen können
3. Im Index sollen die Stoppwörter entfernt werden (Standardliste verwenden)
4. Ich kann Texte nach ihrer Zeichenlänge filtern. Bei der Längenberechnung sollen Stoppwörter mitgezählt werden.
5. Für jeden Text soll die Anzahl Nomen, Verben und wenn möglich Datumsangaben berechnet und angegeben werden.
6. Ich möchte die Texte auf Personen-Namen durchsuchen können
7. Ich möchte die Texte anhand allfällig in den Texten vorhandenen Daten (Datum) einteilen und suchen können (z. B. alle Texte welche etwas mit dem Jahr 2000 zu tun haben auflisten)
8. Ich möchte die Texte basierend auf dem im Text behandelten Thema durchsuchen können

Die Anforderungen werden bis auf zwei Fälle als umsetzbar erachtet.
Anforderung Nr. 1 wird so interpretiert und mit dem Auftraggeber vereinbart, dass die im Datensatz bereits vorhandene
Goldstandard-Zusammenfassung verwendet wird.
Mit einem Modell für extrahierende oder abstrahierende Zusammenfassungen könnten zwar Zusammenfassungen auf Basis des Volltextes
berechnet werden. Sie aber auf eine vordefinierte Anzahl Wörter zu kürzen ist nur mit der abstrahierenden Methode möglicht.
Da das Erstellen eines solchen Modells den zeitlichen Rahmen der Arbeit bei Weitem überschreiten würde, wird darauf verzichtet.

Des Weiteren müsste für die Anforderung Nr. 6 ein Parser für Namen erstellt werden, was ebenfalls ein umfangreiches Unterfangen darstellt.
Stattdessen wird die Anforderung so interpretiert, dass über die Volltextsuche nach Personen gesucht werden kann.

Architektur
-----------
Für ein möglichst einfaches Setup und Deployment wird die Container-Umgebung Docker verwendet.
*docker-compose* ermöglicht es, deklarativ mehrere Container im Verbund gleichzeitig anzusteuern und zu verwalten.
Damit soll es möglich sein, den Index inkl. Preprocessing und GUI einfach und beliebig oft mit dem
Kommando *docker-compose up* zu replizieren.

Per ``docker-compose`` werden drei Container wie folgt erzeugt:

.. figure:: ../images/containers.png
    :align: center

    Docker Compose Architektur


Der Container *Angular-Frontend* enthält einerseits einen NginX-Server und andererseits den Source-Code für das Angular-GUI.
Das GUI ist im Entwicklungsmodus über den Port :8080 und im Produktionsmodus über den HTTP-Port :80 abrufbar.
Da das Angular-Frontend direkten Zugriff auf das Solr-Backend benötigt, leitet Nginx in einer separaten Konfiguration
Anfragen über den Pfad */solr* weiter an den Port :8983 des *Apache-Solr* Containers.
Der Angular-Source-Code sowie die Nginx Konfigurationen werden über Volumes in den Container eingebunden.

Für den *Apache-Solr* Container wird das Original-Image des Herstellers verwendet.
Das Schema für den Index sowie der Index («Core») selbst werden via Volumes mit dem Container verbunden.
Dies ermöglicht dem Container, den Index persistent zu speichern.

Der Container *Python-Scripts* beinhaltet Scripts, die zum einen automatisch den Index aufbauen (falls nicht bereits existent)
und zum anderen ein Topic-Model trainieren bzw. verwenden.
Der Datenfluss und die einzelnen zusätzlichen Datenfelder sind im nächsten Abschnitt beschrieben.
Architektur
===========
Für ein möglichst einfaches Setup und Deployment wird die Container-Umgebung Docker verwendet.
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

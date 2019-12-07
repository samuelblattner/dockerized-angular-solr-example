Requirements
============
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
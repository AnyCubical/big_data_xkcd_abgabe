# Codeabgabe für Big Data Projekt XKCD Crawler

## Tools

- Airflow
- Hadoop
- PySpark
- SQLite
- PHP 7.4
- Apache

## Beschreibung der Aufgabe

Ziel war es mit Hilfe eines automatisierbaren ETL-Workflows alle XKCD-Comics zu crawlen, zu verarbeiten, in eine Datenbank zu packen und mit einem eifachen Web Front-End durchsuchbar zu machen.

Als ETL-Workflow-Tool wurde Airflow gewählt. Zum Speichern der Daten Hadoop und zur Verarbeitung PySpark. Die Ergebnisse werden in einer SQLite Datenbank gespeichert, auf die mit Hilfe einer einfachen PHP-Seite zugegriffen wird.

## Beschreibung des Workflows

Im ersten Schritt muss alle Pfade geleert werden. Um zu gewährleisten, dass die Löschbefehle nicht fehlschlagen, wird eine Platzhalterdatei "placeholder" lokal erzeugt und auf das HDFS kopiert. Anschließend wird der lokale Pfad und der HDFS Pfad parallel geleert. 
Nachdem der lokale Pfad geleert ist, werden alle XKCD-Comics lokal heruntergeladen. Danach können alle Dateien auf das HDFS kopiert werden.
Abschließend werden die Dateien in Pyspark verarbeitet und abgespeichert.

1. create_placeholder
2. copy_hdfs_placeholder
3. clear_xkcddata_hdfs
4. clear_xkcd
5. download_xkcd
6. push_xkcddata_hdfs
7. pyspark_raw_to_final

## Beschreibung des Downloads

Der Download geschieht per Get-Request. Zunächst wird die Nummer des aktuellsten XKCD-Comics herausgefunden. Danach werden per Multiprocessing alle XKCD-Comics mit Hilfe der JSON-API heruntergeladen. Ausgelassen werden dabei die Comics "404", "1037" und "1331", da diese Zeichen beinhalten, die eine CSV-Formatierung durcheinander bringen. Gespeichert werden alle Comics-JSONs nach Jahren partitioniert im HDFS.

## Beschreibung PySpark

In PySpark werden zunächst alle heruntergeladenen Daten aus dem HDFS importiert. Da keine Duplikate enthalten sein werden, werden die Daten nur optimiert. Es werden alle Spalten entfernt, die für die Endbenutzung nicht von Nutzen sind. Benötigt werden nur die Spalten "num", "safe_title", "img" und für eine potentielle Erweiterung der Funktionalität "year". Die Ergebnisse werden sowohl partitioniert als CSV-Datei auf dem HDFS gespeichert, als auch per Pandas in einer SQLite Datenbank.

## Beschreibung Website

Als Webserver wird Apache2 verwendet und für das Backend PHP. In PHP wird eine einfache SQL Query abgesetzt, deren Ergebnisse auf der Seite angezeigt werden. Für eine kleine Verschönerung wird Bootstrap eingebunden.

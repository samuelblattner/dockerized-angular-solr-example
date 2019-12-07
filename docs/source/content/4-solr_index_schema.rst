Solr Index
==========
In diesem Abschnitt wird der Aufbau des Solr-Indexs («Core») beschrieben.


Creating The Core
-----------------
The core is automatically created when the docker container is initialized.
A python script *create_index.py* automatically tries to create the core and exits without error if the core already exists.

.. literalinclude:: ../../../scripts/index/create_index.py
   :language: python
   :lines: 52-69
   :linenos:


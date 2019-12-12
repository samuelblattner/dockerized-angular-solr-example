Angular & Solr on Docker
========================

This is a simple example project using Angular and Apache Solr in a dockerized environment as follows:

![docs/source/images/containers.png](docs/source/images/containers.png)

During initialization, the *Python-Scripts* container will download the raw data from the
[German Summarization Challenge](https://www.swisstext.org/swisstext.org/2019/shared-task/german-text-summarization-challenge.html) (100k text/summary pairs) and index
all texts in a Solr core.

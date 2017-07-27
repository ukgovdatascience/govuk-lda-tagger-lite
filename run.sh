#!/bin/bash

#docker run -i --rm -v ${PWD}/output:/mnt/output ukgovdatascience/govuk-lda-tagger-image:latest --output-topics /mnt/output/default_top25p25_topics.csv --output-tags /mnt/output/default_top25p25_tags.csv --vis-filename /mnt/output/default_top25p25_vis.html --numtopics 25 --use-tfidf  --passes 25 import /mnt/environment_urltext.csv

python train_lda.py --output-topics default_top25p25_topics.csv --output-tags default_top25p25_tags.csv --vis-filename default_top25p25_vis.html --numtopics 3 --passes 1 import environment_urltext_100.csv

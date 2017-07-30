#!/bin/bash

python train_lda.py --output-topics default_top25p25_topics.csv \
    --output-tags default_top25p25_tags.csv \
    --vis-filename default_top25p25_vis.html \
    --numtopics 3 \
    --passes 1 \
    import environment_urltext_100.csv

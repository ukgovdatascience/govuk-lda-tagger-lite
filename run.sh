#!/bin/bash

python train_lda.py --output-topics output/default_top25p25_topics.csv \
    --output-tags output/default_top25p25_tags.csv \
    --vis-filename output/default_top25p25_vis.html \
    --numtopics 3 \
    --passes 1 \
    import input/environment_urltext_100.csv

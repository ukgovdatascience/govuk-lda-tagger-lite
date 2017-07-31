#!/bin/bash

python train_lda.py --output-topics output/topics.csv \
    --output-tags output/tags.csv \
    --vis-filename output/vis.html \
    --numtopics 3 \
    --passes 1 \
    import input/url_text.csv

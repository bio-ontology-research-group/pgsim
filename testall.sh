#!/bin/bash
FILES="data/pairwise_sgd/*.txt"
ROOT="data/pairwise_sgd/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.tsv" ]; then
        echo "Running T test for $filename"
        python test_new.py $filename.txt
    fi
done

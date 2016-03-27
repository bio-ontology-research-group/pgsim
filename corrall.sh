#!/bin/bash
FILES="data/pairwise/*.txt"
ROOT="data/pairwise/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.corr.tsv" ]; then
        echo "Running correlation for $filename"
        python correlation.py $filename.txt
    fi
done

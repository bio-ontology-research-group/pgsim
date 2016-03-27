#!/bin/bash
FILES="data/pairwise/*.txt"
ROOT="data/pairwise/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.tsv" ]; then
        echo "Running T test for $filename"
        python test.py $filename.txt
    fi
done

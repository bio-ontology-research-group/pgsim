#!/bin/bash
FILES="data/pairwise/*.txt"
ROOT="data/pairwise/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.pdf" ]; then
        echo "Plotting the similarity $filename"
        python plot.py $filename.txt
    fi
done

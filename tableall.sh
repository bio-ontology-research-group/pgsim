#!/bin/bash
m="pairwise_sgd"
FILES="data/$m/*.corr.tsv"
ROOT="data/$m/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.pdf" ]; then
        # echo "Running gen_table for $filename"
        echo $filename
        cat data/$m/$filename.tsv
    fi
done

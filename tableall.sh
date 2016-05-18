#!/bin/bash
m="groupwise_new"
FILES="data/$m/*.corr.tsv"
ROOT="data/$m/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.pdf" ]; then
        echo "Running gen_table for $filename"
        python gen_table.py $filename.tsv
    fi
done

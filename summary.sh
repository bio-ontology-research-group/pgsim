#!/bin/bash
FILES="data/groupwise/*.corr.tsv"
ROOT="data/groupwise/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    result=$(tail -n 1 $f)
    echo -e $filename '\t' $result
done

#!/bin/bash
MEASURES=("pairwise_new" "pairwise_sgd" )
for m in ${MEASURES[@]}; do
    echo $m;
    FILES="data/$m/*.txt"
    ROOT="data/$m/"

    for f in $FILES; do
        bname=$(basename "$f")
        filename="${bname%.*}"
        if [ ! -e "$ROOT$filename.diff.tsv" ]; then
            echo "Running correlation for $filename"
            python correlation_sgd.py $m $filename.txt
        fi
    done
done

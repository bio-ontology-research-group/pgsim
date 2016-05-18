#!/bin/bash
MEASURES=("groupwise_sgd" "pairwise_sgd" "groupwise_new" "pairwise_new" "groupwise_depth" "pairwise_depth" )
for m in ${MEASURES[@]}; do
    echo $m;
    FILES="data/$m/*.txt"
    ROOT="data/$m/"

    for f in $FILES; do
        bname=$(basename "$f")
        filename="${bname%.*}"
        if [ ! -e "$ROOT$filename.corr.tsv" ]; then
            echo "Running correlation for $filename"
            python correlation_sgd.py $m $filename.txt
        fi
    done
done

#!/bin/bash
MEASURES=("groupwise_sgd" "pairwise_sgd" "groupwise_new" "pairwise_new" "groupwise_depth" "pairwise_depth")
for m in ${MEASURES[@]}; do
    echo $m;
    FILES="data/$m/*.txt"
    ROOT="data/$m/"

    for f in $FILES; do
        bname=$(basename "$f")
        filename="${bname%.*}"
        if [ ! -e "$ROOT$filename.avg.pdf" ]; then
            echo "Running plot_avg_sim for $filename"
            python plot_avg_sim.py $m $filename.txt
        fi
    done
done

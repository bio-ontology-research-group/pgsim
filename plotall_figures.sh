#!/bin/bash
m="groupwise_new"
FILES="data/$m/*.txt"
ROOT="data/$m/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.pdf" ]; then
        echo "Plotting figures for $filename"
        python plot_figures.py $filename.txt
    fi
done

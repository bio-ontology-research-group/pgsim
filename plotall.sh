#!/bin/bash
FILES="./*.bin"
ROOT="./"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    if [ ! -e "$ROOT$filename.pdf" ]; then
        echo "Converting input"
        java Convert $bname
        echo "Plotting the similarity $filename"
        python plot.py $filename.txt
        rm $filename.txt
    fi
done

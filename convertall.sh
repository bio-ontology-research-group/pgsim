#!/bin/bash
FILES="data/groupwise/*.bin"
ROOT="data/groupwise/"

for f in $FILES; do
    bname=$(basename "$f")
    filename="${bname%.*}"
    echo "Converting $f"
    java Convert $f
done

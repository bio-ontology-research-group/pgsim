#!/bin/bash
for id in {0..7}; do
    groovy SimHPPairwise.groovy $id
done

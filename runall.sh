#!/bin/bash
for id in {0..4}; do
    groovy SimGroupwise.groovy $id
done

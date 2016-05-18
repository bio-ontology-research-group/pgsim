#!/bin/bash
for id in {0..2}; do
    groovy Sim.groovy $id
done

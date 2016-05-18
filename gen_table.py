#!/usr/bin/env python

import sys
import os
import numpy

DATA_ROOT = 'data/'
MEASURES = (
    'groupwise',
    'pairwise',
    'groupwise_sgd',
    'pairwise_sgd',
    'groupwise_new',
    'pairwise_new',)


def main(*args, **kwargs):
    if len(args) < 2:
        raise Exception("Please provide the file name")
    for measure in MEASURES:
        filename = DATA_ROOT + measure + '/' + args[1]
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                next(f)
                spearman = next(f)
                items = spearman.strip().split('\t')
                #next(f)
                #pearson = next(f)
                #items = pearson.strip().split('\t')

                items = [items[0], items[2]]
                for item in items:
                    sys.stdout.write(' & ' + item)
    print ""

if __name__ == '__main__':
    main(*sys.argv)

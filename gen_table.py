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
    # for measure in MEASURES:
    #     filename = DATA_ROOT + measure + '/' + args[1]
    #     if os.path.exists(filename):
    #         with open(filename, 'r') as f:
    #             next(f)
    #             spearman = next(f)
    #             items = spearman.strip().split('\t')
    #             #next(f)
    #             #pearson = next(f)
    #             #items = pearson.strip().split('\t')

    #             items = [items[0], items[2]]
    #             for item in items:
    #                 sys.stdout.write(' & ' + item)
    # print ""
    corrs = list()
    with open('data/correlation_new.txt', 'r') as f:
        for sim in f:
            sim = sim.strip().replace('_', ' ')
            next(f)
            pearson = next(f).strip().split('\t')[0]
            pearson = float(pearson)
            corrs.append((sim, pearson))
    corrs = sorted(corrs, key=lambda x: x[1], reverse=True)
    for item in corrs:
        print '%s & %.6f \\\\' % item

if __name__ == '__main__':
    main(*sys.argv)

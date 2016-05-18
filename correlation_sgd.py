#!/usr/bin/env python
import os
import sys
import numpy as np
from scipy.stats import spearmanr, pearsonr
from data import (
    get_total_average_sims,
    get_diff_average_sims,
    DATA_ROOT)


def get_correlations(measures, filename):
    '''
    Calculates spearman and pearson correlations for
    annotation size with mean and annotation size with variance
    '''
    corrs = list()
    annots, mean, var = get_total_average_sims(measures, filename)
    # annots, mean, var = get_diff_average_sims(measures, filename)
    r1, p1 = spearmanr(annots, mean)
    r2, p2 = spearmanr(annots, var)
    corrs.append((r1, p1, r2, p2))
    r1, p1 = pearsonr(annots, mean)
    r2, p2 = pearsonr(annots, var)
    corrs.append((r1, p1, r2, p2))
    return corrs


def main(*args, **kwargs):
    if len(args) < 3:
        raise Exception('Please provide measures folder and filename')
    measures = args[1]
    filename = args[2]
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    corrs = get_correlations(measures, filename)
    with open(DATA_ROOT + measures + '/' + name + '.corr.tsv', 'w') as f:
        f.write('MEAN_CORR\tPVAL\tVAR_CORR\tPVAL\n')
        for corr in corrs:
            f.write('%f\t%f\t%f\t%f\n' % corr)

if __name__ == '__main__':
    main(*sys.argv)

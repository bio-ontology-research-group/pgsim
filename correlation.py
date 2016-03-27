#!/usr/bin/env python
import os
import sys
import numpy as np
from scipy.stats import spearmanr

DATA_ROOT = 'data/pairwise/'
FILENAME = ''


def load_data(filename):
    data = list()
    with open(DATA_ROOT + filename, 'r') as f:
        for line in f:
            v = float(line.strip())
            data.append(v)
    return data


def get_average_similarities():
    data = load_data(FILENAME)
    m = list()
    v = list()
    for i in range(5):
        for j in range(5):
            s = 0
            for x in range(i * 1000, (i + 1) * 1000):
                for y in range(j * 1000, (j + 1) * 1000):
                    s += data[x * 5000 + y]
            mean = s / 1000000.0
            m.append(mean)
            s = 0
            for x in range(i * 1000, (i + 1) * 1000):
                for y in range(j * 1000, (j + 1) * 1000):
                    t = data[x * 5000 + y] - mean
                    s += t * t
            var = s / 1000000.0
            v.append(var)
    return (m, v)


def get_spearman_correlation():
    mean, var = get_average_similarities()
    annots = [1, 10, 50, 100, 1000]
    ret = list()
    for i in range(5):
        m = mean[i * 5:i * 5 + 5]
        print m
        r1, p1 = spearmanr(annots, m)
        v = var[i * 5:i * 5 + 5]
        print v
        r2, p2 = spearmanr(annots, v)
        ret.append((r1, p1, r2, p2))
    return ret


def get_total_average_sims():
    data = load_data(FILENAME)
    m = list()
    v = list()
    for i in range(5):
        s = 0
        for x in range(i * 1000, (i + 1) * 1000):
            for y in range(5000):
                s += data[x * 5000 + y]
        mean = s / 1000000.0
        m.append(mean)
        s = 0
        for x in range(i * 1000, (i + 1) * 1000):
            for y in range(5000):
                t = data[x * 5000 + y] - mean
                s += t * t
        var = s / 1000000.0
        v.append(var)
    return (m, v)


def get_total_spearman_correlation():
    mean, var = get_total_average_sims()
    annots = [1, 10, 50, 100, 1000]
    r1, p1 = spearmanr(annots, mean)
    r2, p2 = spearmanr(annots, var)
    return (r1, p1, r2, p2)


def main(*args, **kwargs):
    if len(args) < 2:
        raise Exception('Please provide filename')
    filename = args[1]
    global FILENAME
    FILENAME = filename
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    sp = get_spearman_correlation()
    sp.append(get_total_spearman_correlation())
    with open(DATA_ROOT + name + '.corr.tsv', 'w') as f:
        f.write('MEAN_CORR\tPVAL\tVAR_CORR\tPVAL\n')
        for r in sp:
            f.write('%f\t%f\t%f\t%f\n' % r)

if __name__ == '__main__':
    main(*sys.argv)

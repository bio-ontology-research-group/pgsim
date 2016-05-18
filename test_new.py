#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

DATA_ROOT = 'data/pairwise_sgd/'


def get_gene_groups():
    groups = list()
    with open('data/sgd_annotations.txt', 'r') as f:
        for line in f:
            group = len(line.split('\t'))
            groups.append(group)
    return groups

GENE_GROUPS = get_gene_groups()
GENE_NUM = len(GENE_GROUPS)


def load_data(filename):
    data = list()
    with open(DATA_ROOT + filename, 'r') as f:
        for line in f:
            v = float(line.strip())
            data.append(v)
    return data


def get_ttest(data):
    sets = dict()
    for i in range(GENE_NUM):
        for j in range(i + 1, GENE_NUM):
            g1 = GENE_GROUPS[i]
            g2 = GENE_GROUPS[j]
            key = str(g1) + "_" + str(g2)
            if key not in sets:
                sets[key] = list()
            sets[key].append(data[i * GENE_NUM + j])
    results = list()
    keys = list(sets.keys())
    n = len(keys)
    for i in range(n):
        for j in range(i + 1, n):
            s, p = ttest_ind(sets[keys[i]], sets[keys[j]], equal_var=False)
            results.append(
                (keys[i], keys[j], s, p))
    return results


def main(*args, **kwargs):
    if len(args) < 2:
        raise Exception('Please provide filename')
    filename = args[1]
    data = load_data(filename)
    tests = get_ttest(data)
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    with open(DATA_ROOT + name + '.tsv', 'w') as f:
        f.write("Group_1\tGroup_2\tStatistics\tP-value\n")
        for res in tests:
            f.write("%s\t%s\t%f\t%f\n" % res)
if __name__ == '__main__':
    main(*sys.argv)

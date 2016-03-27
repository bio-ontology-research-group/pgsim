#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

DATA_ROOT = 'data/pairwise/'


def load_data(filename):
    data = list()
    with open(DATA_ROOT + filename, 'r') as f:
        for line in f:
            v = float(line.strip())
            data.append(v)
    return data


def get_ttest(data):
    sets = list()
    groups = [1, 10, 50, 100, 1000]
    for i in range(5):
        for j in range(i, 5):
            a = list()
            for x in range(i * 1000, (i + 1) * 1000):
                for y in range(j * 1000, (j + 1) * 1000):
                    a.append(data[x * 5000 + y])
            sets.append((groups[i], groups[j], a))
    results = list()
    n = len(sets)
    for i in range(n):
        for j in range(i + 1, n):
            s, p = ttest_ind(sets[i][2], sets[j][2], equal_var=False)
            results.append((
                sets[i][0], sets[i][1],
                sets[j][0], sets[j][1],
                s, p))
    return results


def get_ttest_total(data):
    sets = list()
    groups = [1, 10, 50, 100, 1000]
    for i in range(5):
        for j in range(i, 5):
            a = list()
            for x in range(i * 1000, (i + 1) * 1000):
                for y in range(j * 1000, (j + 1) * 1000):
                    a.append(data[x * 5000 + y])
            sets.append((groups[i], groups[j], a))
    results = list()
    n = len(sets)
    for i in range(n):
        for j in range(i + 1, n):
            s, p = ttest_ind(sets[i][2], sets[j][2], equal_var=False)
            results.append((
                sets[i][0], sets[i][1],
                sets[j][0], sets[j][1],
                s, p))
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
            f.write("%d-%d\t%d-%d\t%f\t%f\n" % res)
if __name__ == '__main__':
    main(*sys.argv)

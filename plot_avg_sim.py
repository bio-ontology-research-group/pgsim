#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from data import (
    get_total_average_sims,
    get_diff_average_sims,
    DATA_ROOT)


def draw(measures, filename):
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    groups, mean, var = get_total_average_sims(measures, filename)
    # groups, mean, var = get_diff_average_sims(measures, filename)
    # plt.plot(groups, mean)
    plt.errorbar(groups, mean, yerr=var, fmt='o')
    if measures.endswith('depth'):
        plt.xlabel('Annotation depth')
    else:
        plt.xlabel('Annotation size')
    plt.ylabel('Average similarity')
    plt.title(name)
    plt.savefig(DATA_ROOT + measures + '/' + name + '.avg.pdf')


def main(*args, **kwargs):
    if len(args) < 2:
        raise Exception('Please provide filename')
    measures = args[1]
    filename = args[2]
    draw(measures, filename)

if __name__ == '__main__':
    main(*sys.argv)

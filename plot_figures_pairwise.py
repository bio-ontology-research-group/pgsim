#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from data import (
    get_total_average_sims,
    get_diff_average_sims,
    DATA_ROOT)


def get_similarity_name(name):
    name = name.replace('SIM_GROUPWISE_DAG_', '')
    name = name.replace('SIM_GROUPWISE_', '')
    name = name.replace('SIM_FRAMEWORK_DAG_SET_', '')
    name = name.replace('SIM_FRAMEWORK_DAG_', '')
    name = name.replace('SIM_PAIRWISE_DAG_', '')
    name = name.replace('SIM_PAIRWISE_', '')
    return name


def draw(filename):
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    groups1, mean1, var1 = get_diff_average_sims('pairwise_new', filename)
    groups2, mean2, var2 = get_diff_average_sims('pairwise_sgd', filename)
    # groups3, mean3, var3 = get_diff_average_sims('pairwise_hp', filename)
    # groups1, mean1, var1 = get_total_average_sims('pairwise_new', filename)
    # groups2, mean2, var2 = get_total_average_sims('pairwise_sgd', filename)
    # groups3, mean3, var3 = get_total_average_sims('pairwise_hp', filename)
    plt.errorbar(groups1, mean1, yerr=var1, fmt='o', label='synthetic GO')
    plt.errorbar(groups2, mean2, yerr=var2, fmt='o', label='yeast')
    # plt.errorbar(groups3, mean3, yerr=var3, fmt='o', label='synthetic HPO')
    plt.legend()
    plt.xlabel('Annotation size difference')
    plt.ylabel('Average similarity')
    plt.title(get_similarity_name(name))
    plt.savefig(DATA_ROOT + name + '.diff.pdf')


def main(*args, **kwargs):
    if len(args) < 2:
        raise Exception('Please provide filename')
    filename = args[1]
    draw(filename)

if __name__ == '__main__':
    main(*sys.argv)

#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

DATA_ROOT = './'


def load_data(filename):
    data = list()
    with open(DATA_ROOT + filename, 'r') as f:
        for line in f:
            v = float(line.strip())
            data.append(v)
    return data


def get_average_similarities(data):
    sims = list()
    for i in range(5):
        for j in range(5):
            s = 0
            for x in range(i * 1000, (i + 1) * 1000):
                for y in range(j * 1000, (j + 1) * 1000):
                    s += data[x * 5000 + y]
            mean = s / 1000000.0
            s = 0
            for x in range(i * 1000, (i + 1) * 1000):
                for y in range(j * 1000, (j + 1) * 1000):
                    t = data[x * 5000 + y] - mean
                    s += t * t
            var = s / 1000000.0
            sims.append((mean, var))
    return sims


def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


def draw(sims, name):
    N = 5
    groups = list()
    for i in range(N):
        group = list()
        for j in range(N):
            group.append(sims[i * N + j])
        groups.append(group)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.15
    locs = 0.0       # the width of the bars
    colors = ('r', 'y', 'g', 'b', 'k')

    fig, ax = plt.subplots()
    rects = list()
    for i in range(N):
        mean = list()
        var = list()
        for m, v in groups[i]:
            mean.append(m)
            var.append(v)
        rect = ax.bar(
            ind + locs,
            mean, width, color=colors[i], yerr=var)
        locs += 0.15
        rects.append(rect)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Similarities')
    ax.set_title(name)
    ax.set_xticks(ind + (locs - 0.3))
    ax.set_xticklabels(('1', '10', '50', '100', '1000'))

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    legends = list()
    for rect in rects:
        legends.append(rect[0])
    ax.legend(
        legends, ('1', '10', '50', '100', '1000'),
        loc='center left', bbox_to_anchor=(1, 0.5))

    for rect in rects:
        autolabel(ax, rect)


def main(*args, **kwargs):
    if len(args) < 2:
        raise Exception('Please provide filename')
    filename = args[1]
    data = load_data(filename)
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    sims = get_average_similarities(data)
    draw(sims, name)
    plt.savefig(name + '.pdf')

if __name__ == '__main__':
    main(*sys.argv)

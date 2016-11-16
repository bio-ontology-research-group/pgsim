#!/usr/bin/env python
import os
import sys
import numpy as np
from scipy.stats import spearmanr
from utils import get_gene_ontology

DATA_ROOT = 'data/'


def get_annotations():
    gene_ontology = get_gene_ontology()
    annots = dict()
    gene_name = dict()
    with open(DATA_ROOT + 'gene_association.goa_human', 'r') as f:
        for line in f:
            if line[0] == '!':
                continue
            items = line.strip().split('\t')
            if items[3] == 'NOT' or items[6] == 'ND':
                continue
            gene_id = items[1]
            gene_name[gene_id] = items[2]
            go = items[4]
            if go in gene_ontology:
                if gene_id not in annots:
                    annots[gene_id] = set()
                annots[gene_id].add(go)
    groups = dict()
    for gene_id, gos in annots.iteritems():
        l = len(gos)
        if l not in groups:
            groups[l] = list()
        groups[l].append((list(gos), gene_id))
    with open(DATA_ROOT + 'human_annotations_genes.txt', 'w') as f:
        for group in sorted(groups.keys()):
            gos_list = groups[group]
            print group
            for gos, gene_id in gos_list:
                f.write(gene_name[gene_id] + '\t')
                f.write(gos[0])
                for go in gos[1:]:
                    f.write('\t' + go)
                f.write('\n')


def main(*args, **kwargs):
    get_annotations()
    # groups = dict()
    # with open(DATA_ROOT + 'sgd_annotations.txt', 'r') as f:
    #     for line in f:
    #         items = line.split('\t')
    #         group = len(items)
    #         if group not in groups:
    #             groups[group] = 0
    #         groups[group] += 1
    # for group, n in groups.iteritems():
    #     print group, n

if __name__ == '__main__':
    main(*sys.argv)

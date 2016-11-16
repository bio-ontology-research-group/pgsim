#!/usr/bin/env python

import sys
import os
import numpy
import random
from utils import get_gene_ontology, shuffle
from data import get_gene_groups

go = get_gene_ontology()
go_depth = dict()


def get_go_by_depth(go_id, level):
    if go_id not in go or 'is_absolete' in go[go_id]:
        return
    global go_depth
    if level not in go_depth:
        go_depth[level] = set()
    go_depth[level].add(go_id)
    for ch_id in go[go_id]['children']:
        get_go_by_depth(ch_id, level + 1)


def gen_depth_annotations():
    get_go_by_depth('GO:0008150', 1)  # Biological process Ontology
    get_go_by_depth('GO:0005575', 1)  # Cellular component Ontology
    get_go_by_depth('GO:0003674', 1)  # Molecular function Ontology
    with open('data/depth_annotations.txt', 'w') as f:
        for level in go_depth:
            print level
            gos = list(go_depth[level])
            for i in range(100):
                shuffle(gos)
                n = abs(random.randint(2, min(100, len(gos)) - 1))
                f.write(gos[0])
                for go_id in gos[1:n]:
                    f.write('\t' + go_id)
                f.write('\n')


def gen_go_annotations():
    print len(go)
    go_ids = [go_id for go_id in go if 'is_obsolete' not in go[go_id]]
    print len(go_ids)
    print len(go) - len(go_ids)
    shuffle(go_ids)
    with open('data/annotations.txt', 'w') as f:
        for group in range(1, 56):
            for i in range(100):
                shuffle(go_ids)
                f.write(go_ids[0])
                for go_id in go_ids[1:group]:
                    f.write('\t' + go_id)
                f.write('\n')


def gen_hp_annotations():
    cls = list()
    with open('data/hp.txt', 'r') as f:
        for line in f:
            items = line.strip().split()
            cls.append(items[0])
    shuffle(cls)
    with open('data/hp_annotations.txt', 'w') as f:
        for group in range(1, 56):
            for i in range(100):
                shuffle(cls)
                f.write(cls[0])
                for hp_id in cls[1:group]:
                    f.write('\t' + hp_id)
                f.write('\n')


def gen_random_annotations():
    print len(go)
    go_ids = [go_id for go_id in go if 'is_obsolete' not in go[go_id]]
    print len(go_ids)
    print len(go) - len(go_ids)
    shuffle(go_ids)
    groups = get_gene_groups()
    with open('data/mgi_annotations_random.txt', 'w') as f:
        for group in groups:
            shuffle(go_ids)
            f.write(go_ids[0])
            for go_id in go_ids[1:group]:
                f.write('\t' + go_id)
            f.write('\n')


def assign_sgd_random_annots():
    gene_symb = dict()
    with open('data/gene_association.sgd', 'r') as f:
        for line in f:
            if line.startswith('!'):
                continue
            items = line.strip().split('\t')
            gene_symb[items[1]] = items[2]
    annots = dict()
    with open('data/annotations.txt', 'r') as f:
        i = 0
        for line in f:
            items = line.strip().split('\t')
            n = len(items)
            if n not in annots:
                annots[n] = list()
            annots[n].append((items, i))
            i += 1
    genes = dict()
    with open('data/sgd_annotations_genes.txt', 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            gene = items[0]
            n = len(items) - 1
            if n not in genes:
                genes[n] = list()
            genes[n].append(gene_symb[gene])
    with open('data/sgd_annotations_random.txt', 'w') as f:
        for n in sorted(annots.keys()):
            if n not in genes:
                continue
            m = min(len(genes[n]), len(annots[n]))
            for i in range(m):
                gene = genes[n][i]
                items, i = annots[n][i]
                f.write(gene + '\t' + str(i))
                for j in range(len(items)):
                    f.write('\t' + items[j])
                f.write('\n')


def assign_sgd_real_annots():
    gene_ind = dict()
    with open('data/sgd_annotations_genes2.txt', 'r') as f:
        i = 0
        for line in f:
            items = line.strip().split('\t')
            gene_id = items[0]
            gene_ind[gene_id] = i
            i += 1
    with open('data/sgd_annotations_random.txt', 'r') as f:
        with open('data/sgd_annotations_real.txt', 'w') as w:
            for line in f:
                items = line.strip().split('\t')
                gene_id = items[0]
                w.write(gene_id + '\t' + str(gene_ind[gene_id]) + '\n')


def main():
    gen_random_annotations()

if __name__ == '__main__':
    main()

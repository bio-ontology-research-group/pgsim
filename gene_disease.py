#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from sklearn.metrics import roc_curve, auc


def gene_disease():
    gd = dict()
    with open('data/gene_disease/MGI_Geno_Disease.rpt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            items = line.strip().split('\t')
            gene_ids = items[6].split(',')
            dis_ids = items[7].split(',')
            for gene_id in gene_ids:
                for dis_id in dis_ids:
                    if gene_id not in gd:
                        gd[gene_id] = set()
                    gd[gene_id].add(dis_id)
                    if dis_id not in gd:
                        gd[dis_id] = set()
                    gd[dis_id].add(gene_id)
    return gd


def load_scores():
    scores = list()
    with open('data/gene_disease/pairwise/msim_ran_gene_ran_disease.txt') as f:
        for line in f:
            scores.append(float(line.strip()))
    return scores


def load_genes():
    genes = list()
    with open('data/gene_disease/mouse_pheno_annotations_genes.txt') as f:
        for line in f:
            items = line.strip().split('\t')
            genes.append(items[0])
    return genes


def load_diseases():
    diseases = list()
    with open('data/gene_disease/mouse_pheno_annotations_diseases.txt') as f:
        for line in f:
            items = line.strip().split('\t')
            diseases.append(items[0])
    return diseases


def compute_roc(scores, test):
    # Compute ROC curve and ROC area for each class
    fpr, tpr, _ = roc_curve(test, scores)
    roc_auc = auc(fpr, tpr)
    return roc_auc


def main(*args):
    gd = gene_disease()
    scores = load_scores()
    genes = load_genes()
    diseases = load_diseases()
    test = list()
    for g_id in genes:
        for d_id in diseases:
            if g_id in gd and d_id in gd[g_id]:
                test.append(1)
            else:
                test.append(0)
    roc_auc = compute_roc(scores, test)
    print(roc_auc)

if __name__ == '__main__':
    main(*sys.argv)

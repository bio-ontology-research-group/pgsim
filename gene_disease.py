#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from sklearn.metrics import roc_curve, auc
from matplotlib import pyplot as plt
from scipy.stats import spearmanr, pearsonr, wilcoxon


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
    with open('data/gene_disease/pairwise/mouse_sim_gene_disease.txt') as f:
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
    plt.figure()
    plt.plot(
        fpr,
        tpr,
        label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve BMA Resnik - Mouse Gene-Disease Random')
    plt.legend(loc="lower right")
    plt.show()
    return roc_auc


def correlation():
    gd = gene_disease()
    interactions = list()
    annotations = list()
    with open('data/gene_disease/mouse_pheno_annotations_diseases.txt', 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            gene_id = items[0].upper()
            annots = len(items) - 1
            annotations.append(annots)
            if gene_id in gd:
                interactions.append(len(gd[gene_id]))
            else:
                interactions.append(0)
    r, p = pearsonr(annotations, interactions)
    print(r, p)


def main(*args):
    # gd = gene_disease()
    # scores = load_scores()
    # genes = load_genes()
    # diseases = load_diseases()
    # test = list()
    # for g_id in genes:
    #     for d_id in diseases:
    #         if g_id in gd and d_id in gd[g_id]:
    #             test.append(1)
    #         else:
    #             test.append(0)
    # print(sum(test), len(test) - sum(test))
    # roc_auc = compute_roc(scores, test)
    # print(roc_auc)
    correlation()

if __name__ == '__main__':
    main(*sys.argv)

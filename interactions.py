#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from scipy.stats import spearmanr, pearsonr

DATA_ROOT = 'data/pairwise_sgd/'


def get_interactions():
    gene_gene = dict()
    # with open('data/interaction_data.tab', 'r') as f:
    #     for line in f:
    #         if line.startswith('!'):
    #             continue
    #         items = line.strip().split('\t')
    #         gene1_id = items[1]
    #         if not gene1_id:
    #             gene1_id = items[0]
    #         gene2_id = items[3]
    #         if not gene2_id:
    #             gene2_id = items[2]
    #         if gene1_id not in gene_gene:
    #             gene_gene[gene1_id] = set()
    #         if gene2_id not in gene_gene:
    #             gene_gene[gene2_id] = set()
    #         gene_gene[gene1_id].add(gene2_id)
    #         gene_gene[gene2_id].add(gene1_id)

    with open('data/gene_association.sgd', 'r') as f:
        for line in f:
            if line.startswith('!'):
                continue
            items = line.strip().split('\t')
            gene_id = items[1]
            if gene_id not in gene_gene:
                gene_gene[gene_id] = set()
            if items[6] == 'IPI' and items[7]:
                g_ids = items[7].split('|')
                for g_id in g_ids:
                    g_id = g_id.split(':')[1]
                    gene_gene[gene_id].add(g_id)
                    if g_id not in gene_gene:
                        gene_gene[g_id] = set()
                    gene_gene[g_id].add(gene_id)

    genes = set()
    with open('data/sgd_annotations_genes.txt', 'r') as f:
        for line in f:
            gene_id = line.split('\t')[0]
            genes.add(gene_id)

    with open('data/interaction_filtered.txt', 'w') as f:
        for g_id in genes:
            if g_id in gene_gene:
                ints = gene_gene[g_id].intersection(genes)
                if ints:
                    f.write(g_id)
                    for gg_id in ints:
                        f.write('\t' + gg_id)
                    f.write('\n')


def load_interactions():
    gene_gene = dict()
    with open('data/interaction_filtered.txt', 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            gene_gene[items[0]] = set(items[1:])
    return gene_gene


def load_data(filename):
    data = list()
    with open(DATA_ROOT + filename, 'r') as f:
        for line in f:
            line = line.strip()
            data.append(float(line))
    return data


def interactions_scores(data):
    gene_ind = dict()
    gene_int = load_interactions()
    with open('data/sgd_annotations_genes.txt', 'r') as f:
        ind = 0
        for line in f:
            items = line.strip().split('\t')
            gene_ind[items[0]] = ind
            ind += 1

    gene_gene = dict()
    for gene in gene_int.keys():
        if gene not in gene_gene:
            gene_gene[gene] = set()
        x = gene_ind[gene]
        for gene2 in gene_int.keys():
            y = gene_ind[gene2]
            score = data[x * 6108 + y]
            gene_gene[gene].add((gene2, score))
    return gene_gene


def compute_roc():
    data = load_data('SIM_GROUPWISE_BMA_SIM_PAIRWISE_DAG_NODE_RESNIK_1995.txt')
    int_scores = interactions_scores(data)
    ints = load_interactions()
    n = len(int_scores)
    y_score = np.zeros((n, n), dtype='float32')
    y_test = np.zeros((n, n), dtype='float32')
    gene_ind = dict()
    genes = list(set(int_scores.keys()) | set(ints.keys()))
    for ind, gene in enumerate(genes):
        gene_ind[gene] = ind
    for g1 in int_scores:
        for g2, score in int_scores[g1]:
            i = gene_ind[g1]
            j = gene_ind[g2]
            y_score[i, j] = score

    for g1 in ints:
        for g2 in ints[g1]:
            i = gene_ind[g1]
            j = gene_ind[g2]
            y_test[i, j] = 1.0

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    # for i in range(n):
    #     fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    #     roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    # Plot of a ROC curve for a specific class
    plt.figure()
    plt.plot(
        fpr["micro"],
        tpr["micro"],
        label='ROC curve (area = %0.2f)' % roc_auc["micro"])
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve BMA Resnik - yeast')
    plt.legend(loc="lower right")
    plt.show()


def correlation():
    ints = load_interactions()
    interactions = list()
    annotations = list()
    with open('data/sgd_annotations_genes.txt', 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            gene_id = items[0]
            annots = len(items) - 1
            annotations.append(annots)
            if gene_id in ints:
                interactions.append(len(ints[gene_id]))
            else:
                interactions.append(0)
    r, p = pearsonr(annotations, interactions)
    print r, p


def main():
    # compute_roc()
    # get_interactions()
    correlation()

if __name__ == '__main__':
    main()

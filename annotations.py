#!/usr/bin/env python
import os
import sys
import numpy as np
from scipy.stats import spearmanr
from utils import get_obo_ontology

DATA_ROOT = 'data/gene_disease/'


def get_annotations():
    gene_ontology = get_obo_ontology('data/gene_ontology_ext.obo')
    annots = dict()
    gene_name = dict()
    with open(DATA_ROOT + 'gene_association.goa_human', 'r') as f:
        for line in f:
            if line[0] == '!':
                continue
            items = line.strip().split('\t')
            if items[3] == 'NOT' or items[6] == 'ND':
                continue
            gene_id = items[2]
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


def get_phenos():
    phenos = set()
    with open(DATA_ROOT + 'phenos.txt', 'r') as f:
        for line in f:
            pheno = line.strip()
            phenos.add(pheno)
    return phenos


def get_pheno_annotations():
    hp = get_obo_ontology('data/MPheno_OBO.ontology')
    phenos = get_phenos()
    annots = dict()
    with open(DATA_ROOT + 'MGI_PhenoGenoMP.rpt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            items = line.strip().split('\t')
            gene_ids = items[5].split(',')
            ph = items[3]
            if ph in phenos:
                for gene_id in gene_ids:
                    if gene_id not in annots:
                        annots[gene_id] = set()
                    annots[gene_id].add(ph)
    groups = dict()
    for gene_id, phs in annots.iteritems():
        l = len(phs)
        if l not in groups:
            groups[l] = list()
        groups[l].append((list(phs), gene_id))
    with open(DATA_ROOT + 'mouse_pheno_annotations_genes.txt', 'w') as f:
        for group in sorted(groups.keys()):
            gos_list = groups[group]
            print group
            for gos, gene_id in gos_list:
                f.write(gene_id + '\t')
                f.write(gos[0])
                for go in gos[1:]:
                    f.write('\t' + go)
                f.write('\n')


def get_omim_annotations():
    hp = get_obo_ontology('data/hp.obo')
    phenos = get_phenos()
    annots = dict()
    mouse_dis = set()
    with open(DATA_ROOT + 'MGI_Geno_Disease.rpt', 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            mouse_dis |= set(items[7].split(','))
    with open(DATA_ROOT + 'diseases_to_genes_to_phenotypes.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            items = line.strip().split('\t')
            dis_id = items[0]
            if dis_id.startswith('OMIM:'):
                dis_id = dis_id.split(':')[1]
            else:
                continue
            if dis_id not in mouse_dis:
                continue
            ph = items[3]
            if ph in phenos:
                if dis_id not in annots:
                    annots[dis_id] = set()
                annots[dis_id].add(ph)
    groups = dict()
    for gene_id, phs in annots.iteritems():
        l = len(phs)
        if l not in groups:
            groups[l] = list()
        groups[l].append((list(phs), gene_id))
    with open(DATA_ROOT + 'mouse_pheno_annotations_diseases.txt', 'w') as f:
        for group in sorted(groups.keys()):
            gos_list = groups[group]
            print group
            for gos, gene_id in gos_list:
                f.write(gene_id + '\t')
                f.write(gos[0])
                for go in gos[1:]:
                    f.write('\t' + go)
                f.write('\n')


def main(*args, **kwargs):
    get_pheno_annotations()
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

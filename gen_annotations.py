#!/usr/bin/env python

import sys
import os
import numpy
import random
from utils import get_gene_ontology, shuffle

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


def main():
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
    # print len(go)
    # go_ids = [go_id for go_id in go if 'is_obsolete' not in go[go_id]]
    # print len(go_ids)
    # print len(go) - len(go_ids)
    # shuffle(go_ids)
    # with open('data/annotations.txt', 'w') as f:
    #     for group in range(1, 56):
    #         for i in range(100):
    #             shuffle(go_ids)
    #             f.write(go_ids[0])
    #             for go_id in go_ids[1:group]:
    #                 f.write('\t' + go_id)
    #             f.write('\n')


if __name__ == '__main__':
    main()

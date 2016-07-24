import os
import sys


def main(*args, **kwargs):
    with open('data/gene_association.goa_uniprot.tsv', 'r') as f:
        with open('data/gene_association.goa_uniprot.txt', 'w') as w:
            for line in f:
                if not line.startswith('!'):
                    items = line.split('\t')
                    if items[6] != 'IEA':
                        w.write(line)
                else:
                    w.write(line)


if __name__ == '__main__':
    main(*sys.argv)

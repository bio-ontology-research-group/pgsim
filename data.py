import numpy as np

DATA_ROOT = 'data/'


def load_data(measures, filename):
    data = list()
    with open(DATA_ROOT + measures + '/' + filename, 'r') as f:
        for line in f:
            v = float(line.strip())
            data.append(v)
    return data


def get_gene_groups(filename):
    groups = list()
    with open(filename, 'r') as f:
        for line in f:
            group = len(line.split('\t')) - 1
            groups.append(group)
    return groups

# Yeast data
GENE_GROUPS = dict()
GENE_NUM = dict()
GENE_GROUPS['groupwise_sgd'] = GENE_GROUPS['pairwise_sgd'] = get_gene_groups('data/sgd_annotations_genes.txt')
GENE_NUM['groupwise_sgd'] = GENE_NUM['pairwise_sgd'] = len(
    GENE_GROUPS['groupwise_sgd'])

# Random annotations from  1 to 55
GENE_GROUPS['groupwise_new'] = list()
for i in range(1, 56):
    for j in range(0, 100):
        GENE_GROUPS['groupwise_new'].append(i)
GENE_GROUPS['pairwise_new'] = GENE_GROUPS['groupwise_new']
GENE_NUM['groupwise_new'] = GENE_NUM['pairwise_new'] = 5500

# Random annotations from  1 to 55
GENE_GROUPS['groupwise_hp'] = list()
for i in range(1, 56):
    for j in range(0, 100):
        GENE_GROUPS['groupwise_hp'].append(i)
GENE_GROUPS['pairwise_hp'] = GENE_GROUPS['groupwise_hp']
GENE_NUM['groupwise_hp'] = GENE_NUM['pairwise_hp'] = 5500

# Random annotations from  1 to 10
GENE_GROUPS['groupwise_depth'] = list()
for i in range(1, 18):
    for j in range(0, 100):
        GENE_GROUPS['groupwise_depth'].append(i)
GENE_GROUPS['pairwise_depth'] = GENE_GROUPS['groupwise_depth']
GENE_NUM['groupwise_depth'] = GENE_NUM['pairwise_depth'] = 1700

# Random annotations of size 1, 10, 50, 100 and 1000
GENE_GROUPS['groupwise'] = list()
for i in (1, 10, 50, 100, 1000):
    for j in range(1000):
        GENE_GROUPS['groupwise'].append(i)
GENE_GROUPS['pairwise'] = GENE_GROUPS['groupwise']
GENE_NUM['groupwise'] = GENE_NUM['pairwise'] = 5000


def get_total_average_sims(measures, filename):
    data = load_data(measures, filename)
    m = list()
    v = list()
    gene_groups = GENE_GROUPS[measures]
    gene_num = GENE_NUM[measures]
    groups = sorted(list(set(gene_groups)))
    for i in groups:
        jj = list()
        for j in range(gene_num):
            if i == gene_groups[j]:
                jj.append(j)
        s = dict()
        for gr in groups:
            s[gr] = [0.0, 0]
        for x in jj:
            for y in range(gene_num):
                s[gene_groups[y]][0] += data[x * gene_num + y]
                s[gene_groups[y]][1] += 1
        ss = 0.0
        for gr in s:
            s[gr][0] = s[gr][0] / s[gr][1]
            ss += s[gr][0]
        mean = ss / len(s)
        m.append(mean)

        sv = dict()
        for gr in groups:
            sv[gr] = [0.0, 0]
        for x in jj:
            for y in range(gene_num):
                t = data[x * gene_num + y] - s[gene_groups[y]][0]
                sv[gene_groups[y]][0] += t * t
                sv[gene_groups[y]][1] += 1
        ss = 0.0
        for gr in sv:
            sv[gr][0] = sv[gr][0] / sv[gr][1]
            ss += sv[gr][0]
        var = ss / len(sv)
        v.append(var)
    return (groups, m, v)


def get_average_sim(measures, filename, ind):
    data = load_data(measures, filename)
    gene_num = GENE_NUM[measures]
    gene_groups = GENE_GROUPS[measures]
    groups = sorted(list(set(gene_groups)))
    s = dict()
    for gr in groups:
        s[gr] = [0.0, 0]
    for i in range(gene_num):
        s[gene_groups[i]][0] += data[ind * gene_num + i]
        s[gene_groups[i]][1] += 1
    ss = 0.0
    for gr in s:
        s[gr][0] = s[gr][0] / s[gr][1]
        ss += s[gr][0]
    mean = ss / len(s)
    return mean


def get_diff_average_sims(measures, filename):
    data = load_data(measures, filename)
    m = list()
    v = list()
    gene_groups = GENE_GROUPS[measures]
    gene_num = GENE_NUM[measures]

    sims = dict()
    for x in range(gene_num):
        for y in range(gene_num):
            group = abs(gene_groups[x] - gene_groups[y])
            sim = data[x * gene_num + y]
            if group not in sims:
                sims[group] = [0.0, 0]
            sims[group][0] += sim
            sims[group][1] += 1
    for group in sims:
        sims[group] = sims[group][0] / sims[group][1]

    vrs = dict()
    for x in range(gene_num):
        for y in range(gene_num):
            group = abs(gene_groups[x] - gene_groups[y])
            sim = data[x * gene_num + y]
            if group not in vrs:
                vrs[group] = [0.0, 0]
            vr = sim - sims[group]
            vrs[group][0] += vr * vr
            vrs[group][1] += 1
    for group in vrs:
        vrs[group] = vrs[group][0] / vrs[group][1]
    groups = sorted(list(sims.keys()))
    m = list()
    v = list()
    for group in groups:
        m.append(sims[group])
        v.append(vrs[group])
    return (groups, m, v)


if __name__ == '__main__':
    get_total_average_sims('groupwise_sgd', 'SIM_GROUPWISE_DAG_GIC.txt')
    print get_average_sim('groupwise_sgd', 'SIM_GROUPWISE_DAG_GIC.txt', 5)
    print get_average_sim('groupwise_sgd', 'SIM_GROUPWISE_DAG_GIC.txt', 6107)

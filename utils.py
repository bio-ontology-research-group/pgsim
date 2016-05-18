import numpy


def shuffle(*args, **kwargs):
    """
    Shuffle list of arrays with the same random state
    """
    seed = None
    if 'seed' in kwargs:
        seed = kwargs['seed']
    rng_state = numpy.random.get_state()
    for arg in args:
        if seed is not None:
            numpy.random.seed(seed)
        else:
            numpy.random.set_state(rng_state)
        numpy.random.shuffle(arg)


def get_gene_ontology():
    # Reading Gene Ontology from OBO Formatted file
    go = dict()
    obj = None
    with open('data/gene_ontology_ext.obo', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == '[Term]':
                if obj is not None:
                    go[obj['id']] = obj
                obj = dict()
                obj['is_a'] = list()
                continue
            elif line == '[Typedef]':
                obj = None
            else:
                if obj is None:
                    continue
                l = line.split(": ")
                if l[0] == 'id':
                    obj['id'] = l[1]
                elif l[0] == 'is_a':
                    obj['is_a'].append(l[1].split(' ! ')[0])
                elif l[0] == 'is_obsolete' and l[1] == 'true':
                    obj['is_obsolete'] = True
    if obj is not None:
        go[obj['id']] = obj
    for go_id, val in go.iteritems():
        if 'children' not in val:
            val['children'] = list()
        for g_id in val['is_a']:
            if 'children' not in go[g_id]:
                go[g_id]['children'] = list()
            go[g_id]['children'].append(go_id)
    return go

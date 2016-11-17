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


def get_obo_ontology(filename):
    # Reading Ontology from OBO Formatted file
    ont = dict()
    obj = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == '[Term]':
                if obj is not None:
                    ont[obj['id']] = obj
                obj = dict()
                obj['is_a'] = list()
                obj['is_obsolete'] = False
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
        ont[obj['id']] = obj

    for node_id in ont.keys():
        if ont[node_id]['is_obsolete']:
            del ont[node_id]

    for node_id, val in ont.iteritems():
        if 'children' not in val:
            val['children'] = list()
        for n_id in val['is_a']:
            if 'children' not in ont[n_id]:
                ont[n_id]['children'] = list()
            ont[n_id]['children'].append(node_id)
    return ont

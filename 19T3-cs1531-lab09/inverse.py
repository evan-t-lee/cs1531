def inverse(d):
    '''
    Given a dictionary d, invert its structure such that values in d map to lists of keys in d. For example:
    >>> inverse({1: 'A', 2: 'B', 3: 'A'})
    {'A': [1, 3], 'B': [2]}
    '''
    new = {}
    for key, value in d.items():
        new.setdefault(value, set()).add(key)
    return new

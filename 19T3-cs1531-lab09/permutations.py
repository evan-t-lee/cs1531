from itertools import permutations as gen_perms

def permutations(str_in, str_out=''):
    '''
    For the given string, yield all permutations of the characters of that string in any order. For example:
    >>> sorted(list(permutations('ABC')))
    ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']

    If a character occurs more than once in the input string, each occurrence is still considered distinct. For example:
    >>> sorted(list(permutations('ABB')))
    ['ABB', 'ABB', 'BAB', 'BAB', 'BBA', 'BBA']
    '''
    if not str_in:
        yield str_out
    for i in range(len(str_in)):
        new = str_in[:i] + str_in[i+1:]
        yield from permutations(new, str_out + str_in[i])

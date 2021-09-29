# doesn't specify what to do with odd numbers
# current implementation will round up to an even number
def balanced(n, string=''):
    ''' 
    Given a positive number n, yield all strings of length n, in any order, that only contain balanced brackets. For example:
    >>> sorted(list(balanced(6)))
    ['((()))', '(()())', '(())()', '()(())', '()()()']
    '''
    if len(string) >= n:
        yield string
    else:
        if not string.endswith('))'):
            yield from balanced(n, string + '()')
        if string:
            yield from balanced(n, '(' + string +')')
            
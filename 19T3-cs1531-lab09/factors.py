'''
NOTE: This exercise assumes you have completed divisors.py
'''

from divisors import divisors

# You may find this helpful
def is_prime(n):
    return list(divisors(n)) == [1, n]

def factors(n):
    '''
    A generator that yields all the prime factors of n. The prime factors are in ascending order with factors repeated as necessary. For example:
    >>> list(factors(36))
    [2, 2, 3, 3]
    '''
    for i in divisors(n):
        while n != 1 and not n % i and is_prime(i):
            n /= i
            yield i

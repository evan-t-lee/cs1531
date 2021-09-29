from permutations import permutations
from hypothesis import given, strategies, assume
import inspect
import pytest
from math import factorial

def find_divisor(string):
    freq = {c:string.count(c) for c in set(string)}
    total = 1
    for i in freq.values():
        total *= factorial(i)
    return total

def nPr(n, r):
    return factorial(n) / r

def is_perm(string, perm):
    string = list(string)
    for c in perm:
        if c not in string:
            return False
        string.remove(c)
    return True

def check_permutations(string, perms):
    for perm in perms:
        if not is_perm(string, perm):
            return False
    return True

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(permutations), "permutations does not appear to be a generator"

def test_empty():
    assert sorted(list(permutations(''))) == ['']

def test_number():
    with pytest.raises(TypeError) as e:
        sorted(list(permutations(0)))
    assert e

@given(strategies.text(min_size=1,max_size=1))
def test_single(char):
    assert sorted(list(permutations(char))) == [char]

@given(strategies.text(min_size=2,max_size=7))
def test_normal(string):
    perms = sorted(list(permutations(string)))
    assert len(perms) == factorial(len(string))
    assert len(set(perms)) == nPr(len(string), find_divisor(string))
    assert check_permutations(string, perms)

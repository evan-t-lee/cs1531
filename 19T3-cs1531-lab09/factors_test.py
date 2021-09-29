from factors import factors, is_prime
from hypothesis import given, strategies
import inspect
import pytest
import random

def is_prime(n):
    root_n = int(n ** 0.5)
    for i in range(2, root_n + 1):
        if not n % i:
            return False
    return True

def check_factors(n, l):
    total = 1
    for factor in l:
        if not is_prime(factor):
            return False
        total *= factor
    return total == n

def test_generator():
    '''
    Ensure it is generator function.
    '''
    assert inspect.isgeneratorfunction(factors), "factors does not appear to be a generator"

def test_36():
    assert list(factors(36)) == [2, 2, 3, 3]

# Self made tests

def test_0():
    assert list(factors(0)) == []

def test_1():
    assert list(factors(1)) == []

@given(strategies.integers(min_value=-100,max_value=-1))
def test_negative(n):
    assert list(factors(n)) == []

def test_str():
    with pytest.raises(TypeError) as e:
        list(factors('string'))
    assert e

prime_numbers = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
@pytest.mark.parametrize('n', prime_numbers)
def test_prime(n):
    assert list(factors(n)) == [n]

@given(strategies.integers(min_value=2, max_value=100000))
def test_normal(n):
    assert check_factors(n, factors(n))

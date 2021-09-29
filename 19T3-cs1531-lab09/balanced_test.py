from balanced import balanced
from hypothesis import given, strategies
import inspect
import pytest

def is_balanced(string):
    mid_point = int(len(string) / 2)
    for i in range(mid_point):
        if string[i] == string[-i-1]:
            return False
    return True

def check_balanced(strings):
    for string in strings:
        # check only parenthesis exist
        if set(string) != set('()') or not is_balanced(string):
            return False
    return True

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(balanced), "balanced does not appear to be a generator"
    
def test_string():
    with pytest.raises(TypeError) as e:
        list(balanced('a'))
    assert e

def test_empty():
    assert list(balanced(0)) == ['']

# assume only even inputs
@given(strategies.integers(min_value=2,max_value=500))
def test_normal(n):
    if not n % 2:
        strings = sorted(list(balanced(n)))
        assert len(strings) == n / 2
        assert all(len(string) == n for string in strings)
        assert check_balanced(strings)


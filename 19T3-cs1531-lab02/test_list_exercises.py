import pytest
from list_exercises import *

def test_reverse():
    l = [0]
    reverse_list(l)
    assert l == [0]

    l = [-3, -2, -1, 0, 1, 2, 3]
    reverse_list(l)
    assert l == [3, 2, 1, 0, -1, -2, -3]
    # TODO Write more tests for reverse

    l = [] 
    reverse_list(l)
    assert l == []

    l = [1, 2, 3, 3, 2, 1]
    reverse_list(l)
    assert l == [1, 2, 3, 3, 2, 1]

    l = [0, 0, 0, 0]
    assert l == [0, 0, 0, 0]

def test_min():
    assert minimum([0]) == 0
    assert minimum([-3, -2, -1, 0, 1, 2, 3]) == -3
    # TODO Write more tests for minimum

    assert minimum([1, 1, 1, 1]) == 1
    assert minimum([9, 7, -1, 3, -10]) == -10

def test_sum():
    assert sum_list([0]) == 0
    assert sum_list([-3, -2, -1, 0, 1, 2, 3]) == 0
    # TODO Write more tests for sum

    assert sum_list([1, 1, 1, 1]) == 4
    assert sum_list([0, -1, -10, -100]) == -111
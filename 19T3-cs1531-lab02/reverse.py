import pytest
def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is reversed.

    For example,
    >>> reverse_words(["Hello World", "I am here"])
    ['World Hello', 'here am I']
    '''
    return [' '.join(x.split()[::-1]) for x in string_list]

def test_reverse():
    assert reverse_words(['Hello World', 'I am here']) == ['World Hello', 'here am I']
    assert reverse_words(['Omae wa mou shindeiru', 'nani']) == ['shindeiru mou wa Omae', 'nani']
    assert reverse_words(['a b c d', 'e f g h', 'i j k l']) == ['d c b a', 'h g f e', 'l k j i']
    assert reverse_words(['', 'a b', '']) == ['', 'b a', '']
    assert reverse_words(['']) == ['']

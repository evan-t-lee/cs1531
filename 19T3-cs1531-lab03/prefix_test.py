from prefix import prefix_search

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}

def test_no_match():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "c") == {}
    assert prefix_search({"cat": "animal", "apple": "food", "coke": "drink"}, "beer") == {}

def test_contains():
    assert prefix_search({"lorem ipsum": "text", "ipsum lorem": "text", "dolor ipsum": "text"}, "lorem") == {"lorem ipsum": "text"}

def test_number():
    assert prefix_search({"18 legal": "drinking age", "16 legal": "driving age", "21 legal": "US drinking age"}, "2") == {"21 legal": "US drinking age"}

def test_empty():
    assert prefix_search({}, "search string") == {}

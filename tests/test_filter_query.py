from scripts.filter_query import filter_query

def test_filter_match():
    assert filter_query("tests/query/match") == "Match found!"

def test_filter_not_match():
    assert filter_query("tests/query/not_match") == "No match found."
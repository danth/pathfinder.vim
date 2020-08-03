from unittest import mock

from pathfinder.search import search, search_lines, escape


def test_escape():
    assert escape(r"x\x^x$x.x*x[x~x/x") == r"x\\x\^x\$x\.x\*x\[x\~x\/x"


def test_search_finds_shortest_possible_query():
    assert search("abcde", 0, 2) == "c"
    assert search("abcbcde", 0, 3) == "bcd"


def test_search_when_target_is_before_start():
    assert search("abcde", 2, 0) == "a"
    assert search("bcdabc", 3, 0) == "bcd"


@mock.patch("pathfinder.search.search")
def test_search_lines_calls_search_correctly(mock_search):
    search_lines(["a", "bc", "d"], 0, 0, 1, 1)
    mock_search.assert_called_once_with("a\nbc\nd", 0, 3)

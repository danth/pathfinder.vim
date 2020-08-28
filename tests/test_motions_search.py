from unittest import mock

from pathfinder.server.motions import Motion
from pathfinder.server.motions.search import SearchMotionGenerator


def test_escape_magic():
    assert (
        SearchMotionGenerator(None)._escape_magic(r"x\x^x$x.x*x[x~x/x")
        == r"x\\x\^x\$x\.x\*x\[x\~x\/x"
    )


def test_search_finds_shortest_possible_query():
    generator = SearchMotionGenerator(None)
    assert generator._search("abcde", 0, 2) == Motion("/", "c")
    assert generator._search("abcbcdebbc", 0, 3) == Motion("/", "bcd")


def test_search_when_target_is_before_start():
    generator = SearchMotionGenerator(None)
    assert generator._search("abcde", 2, 0) == Motion("/", "a")
    assert generator._search("bcdabc", 3, 0) == Motion("?", "b")


@mock.patch.object(SearchMotionGenerator, "_search")
def test_search_lines_calls_search_correctly(mock_search):
    SearchMotionGenerator(None)._search_lines(["a", "bc", "d"], 0, 0, 1, 1)
    mock_search.assert_called_once_with("a\nbc\nd", 0, 3)

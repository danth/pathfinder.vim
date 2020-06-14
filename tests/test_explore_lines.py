from unittest import mock

from pathfinder.client.explore_lines import get_explore_lines, get_line_limits


def test_get_explore_lines():
    with mock.patch(
        "pathfinder.client.explore_lines.vim.vars",
        {"pf_explore_scale": 0.5, "pf_max_explore": 10},
    ):
        assert get_explore_lines(10) == 5


def test_get_explore_lines_max_0():
    with mock.patch(
        "pathfinder.client.explore_lines.vim.vars",
        {"pf_explore_scale": 0.5, "pf_max_explore": 0},
    ):
        assert get_explore_lines(10) == 0


def test_get_explore_lines_scale_0():
    with mock.patch(
        "pathfinder.client.explore_lines.vim.vars",
        {"pf_explore_scale": 0, "pf_max_explore": 10},
    ):
        assert get_explore_lines(10) == 0


@mock.patch("pathfinder.client.explore_lines.get_explore_lines", return_value=0)
def test_get_line_limits(mock_get_explore_lines):
    with mock.patch("pathfinder.client.explore_lines.vim.current.buffer", ["line"] * 10):
        assert get_line_limits({"lnum": 2}, {"lnum": 8}) == (2, 8)
        assert mock_get_explore_lines.called_once_with(6)


@mock.patch("pathfinder.client.explore_lines.get_explore_lines", return_value=2)
def test_get_line_limits_with_explore(mock_get_explore_lines):
    with mock.patch("pathfinder.client.explore_lines.vim.current.buffer", ["line"] * 10):
        assert get_line_limits({"lnum": 4}, {"lnum": 6}) == (2, 8)
        assert mock_get_explore_lines.called_once_with(4)

import pytest
from unittest import mock

from pathfinder.window import View, winsaveview, winrestview, cursor_in_same_position


TEST_DICT = {"lnum": 0, "col": 10, "curswant": 10, "leftcol": 5, "topline": 0}
TEST_DICT_SOME_STRINGS = {"lnum": 0, "col": "10", "curswant": b"10", "leftcol": 5, "topline": "0"}
TEST_VIEW = View(0, 10, 10, 5, 0)

@mock.patch(
    "pathfinder.window.vim.eval",
    return_value={**TEST_DICT_SOME_STRINGS, "extra values should be ignored": 200},
)
def test_winsaveview(vim_eval):
    assert winsaveview() == TEST_VIEW
    vim_eval.assert_called_once_with("winsaveview()")


@mock.patch("pathfinder.window.vim.eval")
def test_winrestview(vim_eval):
    winrestview(TEST_VIEW)
    vim_eval.assert_called_once_with(f"winrestview({TEST_DICT})")


@pytest.mark.parametrize(
    "view_a,view_b,expected",
    [
        (View(0, 0, None, None, None), View(0, 0, None, None, None), True),
        (View(0, 0, None, None, None), View(1, 0, None, None, None), False),
        (View(0, 0, None, None, None), View(0, 1, None, None, None), False),
        (View(0, 0, None, None, None), View(1, 1, None, None, None), False),
    ],
    ids=["same position", "lnum differs", "col differs", "both differ"],
)
def test_cursor_in_same_position(view_a, view_b, expected):
    assert cursor_in_same_position(view_a, view_b) is expected

import time
from unittest import mock

import pytest

from pathfinder.client.autorun import choose_action
from pathfinder.client.state_tracker import State
from pathfinder.window import View


@pytest.fixture
def default_state():
    return State(View(0, 0, 0, 0, 0), "n", 1, 1, ["hello world"])


def test_choose_action_new_window(default_state):
    assert (
        choose_action(
            default_state._replace(window=1),
            default_state._replace(window=2),
            time.time(),
        )
        == "reset"
    )


@mock.patch("pathfinder.client.autorun.vim.vars", {"pf_autorun_delay": 1})
def test_choose_action_non_motion_mode(default_state):
    assert (
        choose_action(
            default_state._replace(mode="i"),
            default_state._replace(mode="i"),
            time.time(),
        )
        == "reset"
    )


@mock.patch("pathfinder.client.autorun.vim.vars", {"pf_autorun_delay": 1})
def test_choose_action_changed_mode(default_state):
    assert (
        choose_action(
            default_state._replace(mode="n"),
            default_state._replace(mode="i"),
            time.time(),
        )
        == "pathfind"
    )


@mock.patch("pathfinder.client.autorun.vim.vars", {"pf_autorun_delay": 1})
def test_choose_action_changed_lines(default_state):
    assert (
        choose_action(
            default_state._replace(lines=["foo"]),
            default_state._replace(lines=["bar"]),
            time.time(),
        )
        == "pathfind"
    )


@mock.patch("pathfinder.client.autorun.vim.vars", {"pf_autorun_delay": 1})
def test_choose_action_cursor_idle(default_state):
    assert (
        choose_action(
            default_state,
            default_state,
            time.time() - 2,
        )
        == "pathfind"
    )


@mock.patch("pathfinder.client.autorun.vim.vars", {"pf_autorun_delay": 1})
def test_choose_action_set_target(default_state):
    assert (
        choose_action(
            default_state,
            default_state,
            time.time(),
        )
        == "set_target"
    )


@mock.patch("pathfinder.client.autorun.vim.vars", {"pf_autorun_delay": 0})
def test_choose_action_do_nothing(default_state):
    assert (
        choose_action(
            default_state,
            default_state,
            time.time(),
        )
        is None
    )

import pytest
from unittest import mock

from pathfinder.client.state_tracker import StateTracker


@pytest.fixture
def tracker():
    with mock.patch.object(
        StateTracker,
        "_record_state",
        return_value=mock.sentinel.initial_state,
    ):
        return StateTracker()


def test_reset(tracker):
    initial_update_time = tracker.update_time

    with mock.patch.object(
        tracker,
        "_record_state",
        return_value=mock.sentinel.new_state,
    ):
        tracker.reset()

    assert tracker.start_state == mock.sentinel.new_state
    assert tracker.target_state == mock.sentinel.new_state
    assert tracker.update_time > initial_update_time


def test_set_new_target(tracker):
    initial_update_time = tracker.update_time

    with mock.patch.object(
        tracker,
        "_record_state",
        return_value=mock.sentinel.new_state,
    ):
        tracker.set_target()

    assert tracker.start_state == mock.sentinel.initial_state
    assert tracker.target_state == mock.sentinel.new_state
    assert tracker.update_time > initial_update_time


def test_set_same_target(tracker):
    initial_update_time = tracker.update_time

    with mock.patch.object(
        tracker,
        "_record_state",
        return_value=mock.sentinel.initial_state,
    ):
        tracker.set_target()

    assert tracker.start_state == mock.sentinel.initial_state
    assert tracker.target_state == mock.sentinel.initial_state
    assert tracker.update_time == initial_update_time


def test_choose_action_reset(tracker):
    update_time = tracker.update_time

    with mock.patch.object(tracker, "_reset") as reset:
        with mock.patch.object(tracker, "_set_target") as set_target:
            with mock.patch.object(
                tracker,
                "_record_state",
                return_value=mock.sentinel.new_state,
            ):
                chooser = mock.MagicMock(name="chooser", return_value="reset")
                assert tracker.choose_action_using(chooser) == "reset"

            chooser.assert_called_once_with(
                mock.sentinel.initial_state, mock.sentinel.new_state, update_time)
            reset.assert_called_once()
            set_target.assert_not_called()


def test_choose_action_set_target(tracker):
    update_time = tracker.update_time

    with mock.patch.object(tracker, "_reset") as reset:
        with mock.patch.object(tracker, "_set_target") as set_target:
            with mock.patch.object(
                tracker,
                "_record_state",
                return_value=mock.sentinel.new_state,
            ):
                chooser = mock.MagicMock(name="chooser", return_value="set_target")
                assert tracker.choose_action_using(chooser) == "set_target"

            chooser.assert_called_once_with(
                mock.sentinel.initial_state, mock.sentinel.new_state, update_time)
            set_target.assert_called_once()
            reset.assert_not_called()


def test_choose_action_other(tracker):
    update_time = tracker.update_time

    with mock.patch.object(tracker, "_reset") as reset:
        with mock.patch.object(tracker, "_set_target") as set_target:
            with mock.patch.object(
                tracker,
                "_record_state",
                return_value=mock.sentinel.new_state,
            ):
                chooser = mock.MagicMock(name="chooser", return_value="other")
                assert tracker.choose_action_using(chooser) == "other"

            chooser.assert_called_once_with(
                mock.sentinel.initial_state, mock.sentinel.new_state, update_time)
            reset.assert_not_called()
            set_target.assert_not_called()

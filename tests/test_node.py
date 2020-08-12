from unittest import mock
import pytest

from pathfinder.server.node import Node
from pathfinder.server.motions import Motion


def test_reconstruct_path():
    node1 = Node(None, None, None)
    node2 = Node(None, None, mock.sentinel.motion_1)
    node2.set_came_from(node1)
    node3 = Node(None, None, mock.sentinel.motion_2)
    node3.set_came_from(node2)
    node4 = Node(None, None, mock.sentinel.motion_3)
    node4.set_came_from(node3)

    output = node4.reconstruct_path()
    assert output == [
        mock.sentinel.motion_1,
        mock.sentinel.motion_2,
        mock.sentinel.motion_3,
    ]


def test_set_came_from_same_motion():
    node1 = Node(None, None, mock.sentinel.motion_1)
    node2 = Node(None, None, mock.sentinel.motion_1)
    node2.set_came_from(node1)
    assert node2.came_from == node1
    assert node2.came_by_motion_repetitions == 2


def test_set_came_from_different_motion():
    node1 = Node(None, None, mock.sentinel.motion_1)
    node2 = Node(None, None, mock.sentinel.motion_2)
    node2.set_came_from(node1)
    assert node2.came_from == node1
    assert node2.came_by_motion_repetitions == 1


@pytest.mark.parametrize(
    "repetitions,expected",
    [(1, 1), (2, 0), (9, 1), (10, 0), (99, 1)],
    ids=[1, 2, 9, 10, 99],
)
def test_motion_weight_same_motion(repetitions, expected):
    node = Node(None, None, mock.sentinel.motion)
    node.came_by_motion_repetitions = repetitions
    assert node.motion_weight(mock.sentinel.motion) == expected

@pytest.mark.parametrize(
    "motion,expected",
    [(Motion("b", None), 1), (Motion("cd", None), 2), (Motion("e", "fg"), 3)],
    ids=["b", "cd", "e/fg"],
)
def test_motion_weight_different_motion(motion, expected):
    node = Node(None, None, Motion("a", None))
    assert node.motion_weight(motion) == expected

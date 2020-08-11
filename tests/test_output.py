import pytest
from unittest import mock

from pathfinder.client.output import compact_motions, explained_motions, get_count
from pathfinder.server.motions import Motion

COUNTS = [
    ("j", 1, "j"),
    ("j", 2, "jj"),
    ("long", 2, "2long"),
    ("j", 3, "3j"),
    ("j", 10, "10j"),
]


@pytest.mark.parametrize("motion,count,expected", COUNTS, ids=[x[2] for x in COUNTS])
def test_get_count(motion, count, expected):
    motion = Motion(motion, None)
    assert get_count(motion, count) == expected


def test_compact_motions():
    motion1 = Motion("j", None)
    motion2 = Motion("k", None)
    assert compact_motions([motion1, motion2, motion2, motion2]) == "j 3k"


def test_explained_motions():
    motion1 = Motion("j", None)
    motion2 = Motion("f", "g")
    with mock.patch(
        "pathfinder.client.output.vim.vars",
        {"pf_descriptions": {
            "j": "Down {count} lines",
            "f": "To occurence {count} of {argument}"
        }}
    ):
        assert list(explained_motions([motion1, motion2, motion2])) == [
            "j  Down 1 lines",
            "2fg  To occurence 2 of g",
        ]

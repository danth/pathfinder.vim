import pytest

from pathfinder.client.output import compact_motions, explained_motions, get_count
from pathfinder.motion import Motion

COUNTS = [
    ("j", 1, "j"),
    ("j", 2, "jj"),
    ("long", 2, "2long"),
    ("j", 3, "3j"),
    ("j", 10, "10j"),
]


@pytest.mark.parametrize("motion,count,expected", COUNTS, ids=[x[2] for x in COUNTS])
def test_get_count(motion, count, expected):
    motion = Motion(motion, motion, 1, "")
    assert get_count(motion, count) == expected


def test_compact_motions():
    motion1 = Motion("j", "j", 1, "")
    motion2 = Motion("k", "k", 1, "")
    assert compact_motions([motion1, motion2, motion2, motion2]) == "j 3k"


def test_explained_motions():
    motion1 = Motion("j", "j", 1, "Down {count} lines")
    motion2 = Motion("k", "k", 1, "Up {count} lines")
    assert list(explained_motions([motion1, motion2, motion2])) == [
        " j  Down 1 lines",
        "kk  Up 2 lines",
    ]

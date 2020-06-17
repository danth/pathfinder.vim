import pytest

from pathfinder.client.output import compact_motions, explained_motions, get_count
from pathfinder.motion import Motion


COUNTS = [
    ("j", 1, "j"),
    ("j", 2, "jj"),
    ("long", 2, "2long"),
    ("j", 3, "3j"),
    ("j", 10, "10j")
]

@pytest.mark.parametrize("motion,count,expected", COUNTS, ids=[x[2] for x in COUNTS])
def test_get_count(motion, count, expected):
    motion = Motion({"motion": motion.encode(), "weight": 1, "description": "".encode()})
    assert get_count(motion, count) == expected


def test_compact_motions():
    motion1 = Motion({"motion": "j".encode(), "weight": 1, "description": "".encode()})
    motion2 = Motion({"motion": "k".encode(), "weight": 1, "description": "".encode()})
    assert compact_motions([motion1, motion2, motion2, motion2]) == "j 3k"


def test_explained_motions():
    motion1 = Motion(
        {
            "motion": "j".encode(),
            "weight": 1,
            "description": "Down {count} lines".encode(),
        }
    )
    motion2 = Motion(
        {
            "motion": "k".encode(),
            "weight": 1,
            "description": "Up {count} lines".encode(),
        }
    )
    assert list(explained_motions([motion1, motion2, motion2])) == [
        " j  Down 1 lines",
        "kk  Up 2 lines",
    ]

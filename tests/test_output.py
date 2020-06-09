from pathfinder.motion import Motion
from pathfinder.output import compact_motions, explained_motions, get_count


def test_get_count():
    motion = Motion({"motion": "j".encode(), "weight": 1, "description": "".encode()})
    assert get_count(motion, 1) == "j"
    assert get_count(motion, 2) == "2j"
    assert get_count(motion, 10) == "10j"


def test_compact_motions():
    motion1 = Motion({"motion": "j".encode(), "weight": 1, "description": "".encode()})
    motion2 = Motion({"motion": "k".encode(), "weight": 1, "description": "".encode()})
    assert compact_motions([motion1, motion2, motion2]) == "j 2k"


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
        "2k  Up 2 lines",
    ]

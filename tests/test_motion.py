import pytest
from unittest import mock

from pathfinder.motion import motions, Motion

MOTIONS = (
    ({"motion": "j", "weight": 1, "description": "Down"}, Motion("j", "j", 1, "Down")),
    ({"motion": "k".encode(), "weight": 2, "description": "Up"}, Motion("k", "k", 2, "Up")),
    ({"motion": "h", "name": "left", "weight": 1, "description": "Left".encode()}, Motion("h", "left", 1, "Left"))
)


@pytest.mark.parametrize(
    "motion,expected",
    MOTIONS,
    ids=[x[1].motion for x in MOTIONS]
)
def test_motions(motion, expected):
    with mock.patch("pathfinder.motion.vim.vars", {"pf_motions": [motion]}):
        result = list(motions())
        assert len(result) == 1
        assert result[0] == expected


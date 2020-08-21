from collections import namedtuple
from unittest import mock

from pathfinder.server.motions import Motion
from pathfinder.server.motions.find import FindMotionGenerator

View = namedtuple("View", "lnum col curswant")


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
@mock.patch.object(FindMotionGenerator, "_create_node", new=lambda self, v, m: (v, m))
def test_find_f():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 0, 0), "f"))
    assert output == [
        (View(1, 1, 1), Motion("f", "b")),
        (View(1, 2, 2), Motion("f", "c")),
        (View(1, 3, 3), Motion("f", "d")),
        (View(1, 5, 5), Motion("f", "e")),
    ]


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
def test_find_f_final_column():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 5, 5), "f"))
    assert len(output) == 0


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
@mock.patch.object(FindMotionGenerator, "_create_node", new=lambda self, v, m: (v, m))
def test_find_t():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 0, 0), "t"))
    assert output == [
        (View(1, 1, 1), Motion("t", "c")),
        (View(1, 2, 2), Motion("t", "d")),
        (View(1, 4, 4), Motion("t", "e")),
    ]


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
def test_find_t_penultimate_column():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 4, 4), "t"))
    assert len(output) == 0


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
@mock.patch.object(FindMotionGenerator, "_create_node", new=lambda self, v, m: (v, m))
def test_find_F():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 5, 5), "F"))
    assert output == [
        (View(1, 4, 4), Motion("F", "d")),
        (View(1, 2, 2), Motion("F", "c")),
        (View(1, 1, 1), Motion("F", "b")),
        (View(1, 0, 0), Motion("F", "a")),
    ]


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
def test_find_F_first_column():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 0, 0), "F"))
    assert len(output) == 0


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
@mock.patch.object(FindMotionGenerator, "_create_node", new=lambda self, v, m: (v, m))
def test_find_T():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 5, 5), "T"))
    assert output == [
        (View(1, 3, 3), Motion("T", "c")),
        (View(1, 2, 2), Motion("T", "b")),
        (View(1, 1, 1), Motion("T", "a")),
    ]


@mock.patch("pathfinder.server.motions.find.vim.current.buffer", ["abcdde"])
def test_find_T_second_column():
    generator = FindMotionGenerator(None)
    output = list(generator._find(View(1, 1, 1), "T"))
    assert len(output) == 0

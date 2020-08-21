from unittest import mock

from pathfinder.server.motions import Motion
from pathfinder.server.motions.simple import SimpleMotionGenerator

INPUT_VIEW = mock.sentinel.input_view
OUTPUT_VIEW = mock.sentinel.output_view


@mock.patch("pathfinder.server.motions.simple.vim.command")
@mock.patch("pathfinder.server.motions.simple.winsaveview", return_value=OUTPUT_VIEW)
@mock.patch("pathfinder.server.motions.simple.winrestview")
def test_try_motion(winrestview, winsaveview, command):
    generator = SimpleMotionGenerator(None)
    assert generator._try_motion(INPUT_VIEW, "j") == OUTPUT_VIEW
    winrestview.assert_called_once_with(INPUT_VIEW)
    command.assert_called_once_with("silent! normal! j")
    winsaveview.assert_called_once()


@mock.patch("pathfinder.server.motions.simple.vim.command", side_effect=Exception)
@mock.patch("pathfinder.server.motions.simple.winsaveview", return_value=OUTPUT_VIEW)
@mock.patch("pathfinder.server.motions.simple.winrestview")
def test_try_motion_when_motion_raises_exception(winrestview, winsaveview, command):
    generator = SimpleMotionGenerator(None)
    assert generator._try_motion(INPUT_VIEW, "j") is None
    winrestview.assert_called_once_with(INPUT_VIEW)
    command.assert_called_once_with("silent! normal! j")
    winsaveview.assert_not_called()


@mock.patch.object(SimpleMotionGenerator, "_create_node")
@mock.patch.object(SimpleMotionGenerator, "_try_motion", return_value=OUTPUT_VIEW)
def test_generate(try_motion, create_node):
    generator = SimpleMotionGenerator(None)
    output = list(generator.generate(INPUT_VIEW))
    assert len(output) == len(SimpleMotionGenerator.MOTIONS)
    for motion in SimpleMotionGenerator.MOTIONS:
        try_motion.assert_any_call(INPUT_VIEW, motion)
        create_node.assert_any_call(OUTPUT_VIEW, Motion(motion, None))


@mock.patch.object(SimpleMotionGenerator, "_create_node")
@mock.patch.object(SimpleMotionGenerator, "_try_motion", return_value=None)
def test_generate_when_try_motion_returns_none(try_motion, create_node):
    generator = SimpleMotionGenerator(None)
    output = list(generator.generate(INPUT_VIEW))
    assert len(output) == 0
    create_node.assert_not_called()
    for motion in SimpleMotionGenerator.MOTIONS:
        try_motion.assert_any_call(INPUT_VIEW, motion)


@mock.patch.object(SimpleMotionGenerator, "_create_node")
@mock.patch.object(SimpleMotionGenerator, "_try_motion", return_value=INPUT_VIEW)
def test_generate_when_try_motion_returns_same_as_input(try_motion, create_node):
    generator = SimpleMotionGenerator(None)
    output = list(generator.generate(INPUT_VIEW))
    assert len(output) == 0
    create_node.assert_not_called()
    for motion in SimpleMotionGenerator.MOTIONS:
        try_motion.assert_any_call(INPUT_VIEW, motion)

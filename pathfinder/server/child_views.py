import vim

from pathfinder.motion import Motion


def _ftFT(node, motion):
    """
    Yield each view accessible using the given f/t/F/T motion.

    To improve performance, we calculate the view coordinates directly, rather than
    testing the motion inside Vim. Since f/t/F/T only ever work inside a single line,
    we only need to update the column number.
    """
    line_text = vim.current.buffer[node.view["lnum"] - 1]
    # characters = string of characters which may be accessible using this motion
    # column = lambda function which converts index in `characters` to a column number
    if motion.motion == 'f':
        column = lambda i: node.view["col"] + i + 1
        characters = line_text[node.view["col"] + 1:]
    elif motion.motion == 't':
        column = lambda i: node.view["col"] + i + 1
        characters = line_text[node.view["col"] + 2:]
    elif motion.motion == 'F':
        column = lambda i: node.view["col"] - i - 1
        # Characters are reversed because we are looking backwards
        characters = line_text[:node.view["col"]][::-1]
    elif motion.motion == 'T':
        column = lambda i: node.view["col"] - i - 1
        characters = line_text[:node.view["col"] - 1][::-1]

    seen_characters = set()
    for i, character in enumerate(characters):
        # Only use each unique character once
        if character in seen_characters:
            continue
        seen_characters.add(character)

        # Insert character into the name and description
        new_motion = Motion(
            motion.motion + character,
            motion.name + character,
            motion.weight,
            motion.description_template.replace("{char}", character)
        )
        # Calculate the resulting position
        new_view = node.view.copy()
        new_view["col"] = new_view["curswant"] = column(i)
        yield new_motion, new_view


def _all_child_views(node, available_motions):
    for motion in available_motions:
        if motion.motion in "ftFT":
            yield from _ftFT(node, motion)
        else:
            yield motion, node.test_motion(motion)


def child_views(node, available_motions, min_line, max_line):
    """
    Yield each child view found using the given list of motions.

    This will be in the form (motion, resulting view).

    :param node: Node to find children of.
    :param available_motions: List of motions available for use.
    :param min_line: Results above this line number will be ignored.
    :param max_line: Results below this line number will be ignored.
    """
    for motion, child_view in _all_child_views(node, available_motions):
        if (
            child_view is not None
            and child_view["lnum"] >= min_line
            and child_view["lnum"] <= max_line
        ):
            yield motion, child_view

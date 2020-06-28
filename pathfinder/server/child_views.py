import vim

from pathfinder.motion import Motion
from pathfinder.window import View, cursor_in_same_position, winrestview, winsaveview


def _ftFT(view, motion):
    """
    Yield each view accessible using the given f/t/F/T motion.

    To improve performance, we calculate the view coordinates directly, rather than
    testing the motion inside Vim. Since f/t/F/T only ever work inside a single line,
    we only need to update the column number.
    """
    line_text = vim.current.buffer[view.lnum - 1]
    seen_characters = set()

    # characters = string of characters which may be accessible using this motion
    # column = lambda function which converts index in `characters` to a column number
    if motion.motion == "f" and view.col <= len(line_text):
        column = lambda i: view.col + i + 1
        characters = line_text[view.col + 1 :]
    elif motion.motion == "t" and view.col < len(line_text) - 1:
        column = lambda i: view.col + i + 1
        characters = line_text[view.col + 2 :]
        seen_characters.add(line_text[view.col + 1])
    elif motion.motion == "F" and view.col > 0:
        column = lambda i: view.col - i - 1
        # Characters are reversed because we are looking backwards
        characters = line_text[: view.col][::-1]
    elif motion.motion == "T" and view.col > 1:
        column = lambda i: view.col - i - 1
        characters = line_text[: view.col - 1][::-1]
        seen_characters.add(line_text[view.col - 1])
    else:
        return

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
            motion.description_template.replace("{char}", character),
        )
        # Calculate the resulting position
        new_col = column(i)
        new_view = view._replace(col=new_col, curswant=new_col)

        yield new_motion, new_view


def _test_motion(view, motion):
    """
    Yield the resulting view of a motion, by testing it inside Vim.

    :returns: New view, if the cursor moved and no errors were caused. Otherwise None.
    """
    winrestview(view)
    try:
        # execute is required to use motions like <C-f>
        vim.command(f'execute "silent! normal! {motion.motion}"')
    except vim.error:
        # Ignore motions which fail
        return

    new_view = winsaveview()
    if not cursor_in_same_position(new_view, view):
        return new_view


def _all_child_views(view, available_motions):
    for motion in available_motions:
        if motion.motion in "ftFT":
            yield from _ftFT(view, motion)
        else:
            yield motion, _test_motion(view, motion)


def child_views(view, available_motions, min_line, max_line):
    """
    Yield each child view found using the given list of motions.

    This will be in the form (motion, resulting view).

    :param view: View to find children of.
    :param available_motions: List of motions available for use.
    :param min_line: Results above this line number will be ignored.
    :param max_line: Results below this line number will be ignored.
    """
    for motion, child_view in _all_child_views(view, available_motions):
        if (
            child_view is not None
            and child_view.lnum >= min_line
            and child_view.lnum <= max_line
        ):
            yield motion, child_view

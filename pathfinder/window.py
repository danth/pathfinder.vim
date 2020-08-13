from collections import namedtuple

import vim

View = namedtuple("View", "lnum col curswant leftcol topline")


def winsaveview():
    view_dict = vim.eval("winsaveview()")
    # Any dictionary elements not in View._fields will be discarded
    return View._make(int(view_dict[field]) for field in View._fields)


def winrestview(view):
    view_dict = dict(view._asdict())
    vim.eval(f"winrestview({view_dict})")


def cursor_in_same_position(a, b):
    """
    Check if the given views have the cursor on the same position.

    The scroll position and other properties may differ.
    """
    return a.lnum == b.lnum and a.col == b.col

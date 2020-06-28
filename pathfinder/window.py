from collections import namedtuple

import vim


# We create this namedtuple based on a real winsaveview()
# in case an additional property is added in a future Vim.
dummy_view = vim.eval("winsaveview()")
View = namedtuple("View", dummy_view.keys())


def winsaveview():
    view_dict = vim.eval("winsaveview()")
    view_dict = {k: int(v) for k, v in view_dict.items()}
    return View(**view_dict)


def winrestview(view):
    view_dict = dict(view._asdict())
    vim.eval(f"winrestview({view_dict})")


def cursor_in_same_position(a, b):
    """
    Check if the given views have the cursor on the same position.

    The scroll position and other properties may differ.
    """
    return a.lnum == b.lnum and a.col == b.col

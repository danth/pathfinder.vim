import vim


def winsaveview():
    return vim.eval("winsaveview()")


def winrestview(view):
    f = vim.Function("winrestview")
    f(view)


def cursor_in_same_position(a, b):
    """
    Check if the given views have the cursor on the same position.

    The scroll position and other properties may differ.
    """
    return a["lnum"] == b["lnum"] and a["col"] == b["col"]

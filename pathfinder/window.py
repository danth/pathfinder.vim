import vim


def winsaveview():
    return {k: int(v) for k, v in vim.eval("winsaveview()").items()}


def winrestview(view):
    vim.eval(f"winrestview({view})")


def cursor_in_same_position(a, b):
    """
    Check if the given views have the cursor on the same position.

    The scroll position and other properties may differ.
    """
    return a["lnum"] == b["lnum"] and a["col"] == b["col"]

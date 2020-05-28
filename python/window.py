import vim


def winsaveview():
    return vim.bindeval("winsaveview()")


def winrestview(view):
    vim.current.window.vars["view_to_restore"] = view
    vim.eval("winrestview(w:view_to_restore)")
    del vim.current.window.vars["view_to_restore"]


def cursor_in_same_position(a, b):
    """
    Check if the given views have the cursor on the same position.

    The scroll position and other properties may differ.
    """
    return a["lnum"] == b["lnum"] and a["col"] == b["col"]

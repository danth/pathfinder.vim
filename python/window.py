import vim


def winsaveview():
    return vim.bindeval("winsaveview()")


def winrestview(view):
    vim.current.window.vars["view_to_restore"] = view
    vim.eval("winrestview(w:view_to_restore)")
    del vim.current.window.vars["view_to_restore"]

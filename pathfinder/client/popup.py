import vim

from pathfinder.debytes import debytes


def _neovim_popup(text, line_offset):
    """Create a popup using Neovim 0.4+ floating windows."""
    # Insert text into a scratch buffer
    buffer = vim.api.create_buf(False, True)
    vim.api.buf_set_lines(buffer, 0, -1, True, [f" {text} "])

    # Create a window containing the buffer
    window = vim.api.open_win(buffer, 0, {
        "relative": "cursor",
        "row": int(line_offset),
        "col": 0,
        "style": "minimal",
        "focusable": 0,
        "height": 1,
        "width": len(text) + 2,
    })
    # Set the highlight of the window to match the cursor
    vim.api.win_set_option(window, 'winhl', 'Normal:PathfinderPopup')

    # Create a timer to close the window
    popup_time = int(vim.vars["pf_popup_time"])
    vim.eval(f"timer_start({popup_time}, {{-> nvim_win_close({window.handle}, 1)}})")


def _vim_popup(text, line_offset):
    """Create a popup using Vim +popupwin."""
    vim.Function("popup_create")(
        text,
        {
            "line": f"cursor{line_offset}",
            "col": "cursor",
            "wrap": False,
            "padding": (0, 1, 0, 1),
            "highlight": "PathfinderPopup",
            "time": int(vim.vars["pf_popup_time"]),
            "zindex": 1000,
        },
    )


def open_popup(text):
    line_offset = "+1" if vim.eval("line('.')") == "1" else "-1"

    if vim.eval("has('nvim-0.4')") == "1":
        _neovim_popup(text, line_offset)
    elif vim.eval("has('popupwin')") == "1":
        _vim_popup(text, line_offset)
    else:
        # Not able to create a popup
        print(text)

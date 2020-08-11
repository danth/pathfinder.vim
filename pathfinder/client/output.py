import itertools

import vim

from pathfinder.debytes import debytes

last_output = None


def get_count(motion, count):
    """Build a string like 'k', 'hh', '15w'"""
    motion_str = motion.motion + (motion.argument or "")
    if count == 1:
        return motion_str

    elif count == 2 and len(motion_str) == 1:
        # It's easier to press a single-character motion twice
        # than to type a 2 before it
        return (motion_str) * 2

    return str(count) + motion_str


def compact_motions(motions):
    """
    Return the given motion sequence in single-line form.

    e.g. 2* 5j $
    """
    return " ".join(
        [
            get_count(motion, len(list(group)))
            for motion, group in itertools.groupby(motions)
        ]
    )


def get_description(motion, repetitions):
    description = debytes(vim.vars["pf_descriptions"][motion.motion])
    description = description.replace("{count}", str(repetitions))
    if motion.argument is not None:
        description = description.replace("{argument}", motion.argument)
    return description


def explained_motions(motions):
    """
    Yield each motion in the form "motion <padding> help"

    e.g. ['5j   Down 5 lines', '$    To the end of the line']
    """
    for motion, group in itertools.groupby(motions):
        repetitions = len(list(group))
        yield (
            get_count(motion, repetitions) + "  " + get_description(motion, repetitions)
        )


def show_output(motions):
    global last_output
    last_output = motions

    win_line = "+1" if vim.eval("line('.')") == "1" else "-1"
    if int(vim.eval("has('nvim-0.4')")):
        ## Neovim >=0.4 floating windows ##
        # There is no padding option so we add it ourselves
        text = " " + compact_motions(motions) + " "
        # Insert text into a scratch buffer
        escaped_text = text.replace("'", r"\'")
        buf_nr = vim.eval("nvim_create_buf(v:false, v:true)")
        vim.eval(
            f"nvim_buf_set_lines({buf_nr}, 0, {win_line}, v:true, ['{escaped_text}'])"
        )

        # Create a window containing the buffer
        window_options = {
            "relative": "cursor",
            "row": int(win_line),
            "col": 0,
            "style": "minimal",
            "focusable": 0,
            "height": 1,
            "width": len(text),
        }
        win_nr = vim.eval(f"nvim_open_win({buf_nr}, 0, {window_options})")
        # Set the highlight of the window to match the cursor
        vim.eval(f"nvim_win_set_option({win_nr}, 'winhl', 'Normal:PathfinderPopup')")

        # Create a timer to close the window
        popup_time = int(vim.vars["pf_popup_time"])
        vim.eval(f"timer_start({popup_time}, {{-> nvim_win_close({win_nr}, 1)}})")
    elif int(vim.eval("has('popupwin')")):
        ## Vim with +popupwin ##
        # Much simpler than the Neovim equivalent!
        vim.Function("popup_create")(
            compact_motions(motions),
            {
                "line": f"cursor{win_line}",
                "col": "cursor",
                "wrap": False,
                "padding": (0, 1, 0, 1),
                "highlight": "PathfinderPopup",
                "time": int(vim.vars["pf_popup_time"]),
                "zindex": 1000,
            },
        )
    else:
        ## Vim without +popupwin / Neovim <0.4 ##
        print(compact_motions(motions))

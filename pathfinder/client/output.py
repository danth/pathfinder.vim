import itertools

import vim

last_output = None


def get_count(motion, count):
    """Build a string like 'k', 'hh', '15w'"""
    if count == 1:
        return motion.name

    elif count == 2 and len(motion.name) == 1:
        # It's easier to press a single-character motion twice
        # than to type a 2 before it
        return motion.name + motion.name

    return str(count) + motion.name


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


def explained_motions(motions):
    """
    Yield each motion in the form "motion <padding> help"

    e.g. ['5j   Down 5 lines', '$    To the end of the line']
    """
    # List of tuples of (count, count combined with motion, Motion instance)
    counted_motions = list()
    for motion, group in itertools.groupby(motions):
        repetitions = len(list(group))
        counted = get_count(motion, repetitions)
        counted_motions.append((repetitions, counted, motion))

    # Maximum length of the '5j', '$' etc. strings
    max_counted_len = max(len(c[1]) for c in counted_motions)

    for repetitions, counted, motion in counted_motions:
        padding = " " * (max_counted_len - len(counted))
        description = motion.description_template.replace("{count}", str(repetitions))
        yield padding + counted + "  " + description


def show_output(motions):
    global last_output
    last_output = motions

    if int(vim.eval("has('nvim-0.4')")):
        ## Neovim >=0.4 floating windows ##
        # There is no padding option so we add it ourselves
        text = " " + compact_motions(motions) + " "
        # Insert text into a scratch buffer
        escaped_text = text.replace("'", r"\'")
        buf_nr = vim.eval("nvim_create_buf(v:false, v:true)")
        vim.eval(f"nvim_buf_set_lines({buf_nr}, 0, -1, v:true, ['{escaped_text}'])")

        # Create a window containing the buffer
        window_options = {
            "relative": "cursor",
            "row": -1,
            "col": 0,
            "style": "minimal",
            "focusable": 0,
            "height": 1,
            "width": len(text),
        }
        win_nr = vim.eval(f"nvim_open_win({buf_nr}, 0, {window_options})")
        # Set the highlight of the window to match the cursor
        vim.eval(f"nvim_win_set_option({win_nr}, 'winhl', 'Normal:Cursor')")

        # Create a timer to close the window
        popup_time = int(vim.vars["pf_popup_time"])
        vim.eval(f"timer_start({popup_time}, {{-> nvim_win_close({win_nr}, 1)}})")
    elif int(vim.eval("has('popupwin')")):
        ## Vim with +popupwin ##
        # Much simpler than the Neovim equivalent!
        vim.Function("popup_create")(
            compact_motions(motions),
            {
                "line": "cursor-1",
                "col": "cursor",
                "wrap": False,
                "padding": (0, 1, 0, 1),
                "highlight": "Cursor",
                "time": int(vim.vars["pf_popup_time"]),
                "zindex": 1000,
            },
        )
    else:
        ## Vim without +popupwin / Neovim <0.4 ##
        print(compact_motions(motions))

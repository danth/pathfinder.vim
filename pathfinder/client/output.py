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

    if int(vim.eval("has('nvim')")):
        print(compact_motions(motions))
    elif int(vim.eval("has('popupwin')")):
        vim.Function("popup_create")(
            compact_motions(motions),
            {
                "line": "cursor-1",
                "col": "cursor",
                "wrap": False,
                "padding": (0, 1, 0, 1),
                "highlight": "Cursor",
                "time": 3000,
                "zindex": 1000,
            },
        )
    else:
        print(compact_motions(motions))

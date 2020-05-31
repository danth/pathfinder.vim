import itertools

import vim


def count(motion, count):
    """Build a string like 'k', '2h', '15w'"""
    # Add a count only if there is more than 1 repetition
    return (str(count) if count > 1 else "") + motion.motion


def compact_motions(motions):
    """
    Return the given motion sequence in single-line form.

    e.g. 2* 5j $
    """
    return " ".join(
        [
            count(motion, len(list(group)))
            for motion, group in itertools.groupby(motions)
        ]
    )


def explained_motions(motions):
    """
    Yield each motion in the form "motion <padding> help"

    e.g. ['5j   Down 5 lines', '$    To the end of the line']
    """
    for motion, group in itertools.groupby(motions):
        repetitions = len(list(group))
        counted = count(motion, repetitions)
        padding = " " * (5 - len(counted))
        yield counted + padding + motion.description(repetitions)


def output(motions):
    if vim.eval("has('nvim')"):
        print(compact_motions(motions))
    elif vim.eval("has('popupwin')"):
        output = list(explained_motions(motions))
        vim.Function("popup_create")(
            output,
            {
                # 4 lines up from the bottom of the screen
                "line": vim.options["lines"] - 4,
                # No "col" option = centered on screen
                # Make the "line" option relative to the bottom edge
                "pos": "botleft",
                "wrap": False,
                "padding": (0, 1, 0, 1),
                "time": 3000 + (500 * len(output)),
            },
        )
    else:
        print(compact_motions(motions))

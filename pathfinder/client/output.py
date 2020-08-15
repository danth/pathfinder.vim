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

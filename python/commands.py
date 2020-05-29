import itertools

import vim
from pathfinder import find_path
from window import cursor_in_same_position, winrestview, winsaveview


def pathfinder_run():
    start = vim.current.buffer.vars["pf_start"]
    target = winsaveview()

    if cursor_in_same_position(start, target):
        return print("No motions used")

    motions = find_path(start, target)

    # Restore the cursor to where it was when :PathfinderBegin was ran
    winrestview(start)

    for motion, group in itertools.groupby(motions):
        repetitions = len(list(group))
        # Add a count only if there is more than 1 repetition
        motion_str = (str(repetitions) if repetitions > 1 else "") + motion.motion

        # Pad all motions to 5 characters wide so the descriptions are aligned
        padding = " " * (5 - len(motion_str))
        print(motion_str, motion.description(repetitions), sep=padding)

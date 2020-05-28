import vim
import itertools

from window import winsaveview, winrestview
from pathfinder import find_path


def pathfinder_run():
    start = vim.current.buffer.vars["pf_start"]
    target = winsaveview()

    motions = find_path(start, target)

    # Restore the cursor to where it was when :PathfinderBegin was ran
    winrestview(start)

    output = ""
    for motion, group in itertools.groupby(motions):
        repetitions = len(list(group))
        # Add a count only if there is more than 1 repetition
        output += str(repetitions) if repetitions > 1 else ""
        output += motion.motion

    print(output)


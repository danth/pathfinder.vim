import itertools

import vim
from client import client
from window import cursor_in_same_position, winrestview, winsaveview


start = None


def pathfinder_begin():
    global start
    start = winsaveview()
    print("Move to target location and then :PathfinderRun")


def display_results(motions):
    output = ""
    for motion, group in itertools.groupby(motions):
        repetitions = len(list(group))
        # Add a count only if there is more than 1 repetition
        # Builds a string like "2k", "15w"
        motion_str = (str(repetitions) if repetitions > 1 else "") + motion.motion

        # Pad all motions to 5 characters wide so the descriptions are aligned
        padding = " " * (5 - len(motion_str))
        output += motion_str + padding + motion.description(repetitions) + "\n"

    # Printing multiple lines doesn't make a hit-enter prompt appear so we
    # pass the string to the echo command instead
    # replace(', \') escapes ' characters
    vim.command("echo \"" + output.replace("'", "\\'") + '"')

def pathfinder_run():
    if start is None:
        return print("Please run :PathfinderBegin to set a start position first")

    target = winsaveview()
    if cursor_in_same_position(start, target):
        return print("No motions required")

    client.pathfind(start, target, display_results)

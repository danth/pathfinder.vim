import itertools
import time

import vim
from client import client  # Importing this will start the server
from window import cursor_in_same_position, winrestview, winsaveview


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


class RecordedState:
    """
    A snapshot of useful information at a specific time.

    Used for comparing the start of a path to the current state to determine whether
    pathfinding should begin.
    """
    def __init__(self):
        self.time = time.time()
        self.view = winsaveview()
        self.mode = vim.eval("mode()")
        self.buffer_contents = vim.eval("getline(0,'$')")


def reset():
    """
    Reset variables ready for a new movement.

    This is called after run(), and to cancel a path on events such as BufNewFile.
    """
    global start_state, current_state
    start_state = RecordedState()
    current_state = start_state


def run():
    """
    Start calculating a path.

    This is called by loop() below, when there are no motions for a while. It also
    runs for a variety of autocmd events which indicate the end of a movement, such as
    entering insert mode.
    """
    if start_state is None or current_state is None:
        return

    if not cursor_in_same_position(start_state.view, current_state.view):
        # Start pathfinding in the background and call display_results when done
        client.pathfind(start_state.view, current_state.view, display_results)

    reset()


def loop():
    """Called on a timer several times per second."""
    # If the server is disconnected: Attempt to connect
    # If the server is connected: Process responses
    client.poll_responses()

    global start_state, current_state
    new_state = RecordedState()

    if (
        time.time() >= current_state.time + vim.vars["pf_autorun_delay"]
        # This is checked in run(), but that would reset the timer if we called it
        and not cursor_in_same_position(start_state.view, current_state.view)
    ):
        # No motions for the configured timeout
        run()
    elif start_state.mode in ['n', 'v', 'V'] and start_state.mode != new_state.mode:
        # Changed modes, leaving one of normal, visual or visual-line
        # (we don't want to trigger for leaving e.g. insert mode since cursor
        # movements there are not made with motions)
        run()
    elif (
        new_state.mode == 'n' and
        new_state.buffer_contents != start_state.buffer_contents
    ):
        # Buffer has changed in normal mode
        # This means a command like x,rx,p must have been used
        run()
    elif not cursor_in_same_position(current_state.view, new_state.view):
        current_state = new_state


# Call reset to set the initial state
reset()

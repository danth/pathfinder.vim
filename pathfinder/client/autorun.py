import time

import vim


def choose_action(start_state, current_state, update_time):
    """
    Select an action to take automatically.

    This is intended for use with StateTracker.choose_action_using().

    Returns one of:
    "reset" - Set start and target to the current state
    "set_target" - Set target to the current state
    "pathfind" - Start pathfinding, using the target from last time it was set
    None - Do nothing
    """
    if (
        start_state.window != current_state.window
        or start_state.buffer != current_state.buffer
    ):
        # Reset to ensure the start or target view isn't set to a location
        # which is now impossible to access
        return "reset"

    delay = vim.vars["pf_autorun_delay"]
    if delay > 0:  # If delay <= 0, then the user disabled autorun
        if start_state.mode not in {"n", "v", "V", ""}:
            # Motions are not used in this mode, so pathfinding is useless
            return "reset"

        if (
            time.time() >= update_time + delay
            or start_state.mode != current_state.mode
            or start_state.lines != current_state.lines
        ):
            return "pathfind"
        else:
            return "set_target"


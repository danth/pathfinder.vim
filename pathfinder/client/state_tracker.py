import time
from collections import namedtuple

import vim

from pathfinder.window import winsaveview

State = namedtuple("State", "view mode buffer window lines")


class StateTracker:
    def __init__(self):
        self.reset()

    def _set_update_time(self):
        self.update_time = time.time()

    def _record_state(self):
        return State(
            winsaveview(),
            vim.eval("mode()"),
            vim.current.buffer.number,
            vim.current.window.number,
            vim.current.buffer[:],
        )

    def reset(self):
        current_state = self._record_state()
        self._reset(current_state)

    def _reset(self, new_state):
        self.start_state = new_state
        self.target_state = new_state
        self._set_update_time()

    def set_target(self):
        current_state = self._record_state()
        self._set_target(current_state)

    def _set_target(self, new_state):
        if new_state != self.target_state:
            self.target_state = new_state
            self._set_update_time()

    def choose_action_using(self, function):
        """
        Choose an action to take using the given function.

        Function will be called with the arguments (start state, current state,
        time of most recent update). It may return "reset" or "set_target" to
        call the corresponding method, or any other value to do nothing.  The
        function's return value is passed through this method, so can be used
        to take further actions elsewhere.
        """
        current_state = self._record_state()

        result = function(self.start_state, current_state, self.update_time)
        if result == "reset":
            self._reset(current_state)
        elif result == "set_target":
            self._set_target(current_state)

        return result

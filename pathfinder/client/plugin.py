import time

import vim

import pathfinder.client.output as output
from pathfinder.client.autorun import choose_action
from pathfinder.client.client import Client
from pathfinder.client.popup import open_popup
from pathfinder.client.state_tracker import StateTracker
from pathfinder.window import cursor_in_same_position


class Plugin:
    def __init__(self):
        self.client = Client()
        self.state_tracker = StateTracker()
        self.last_output = None

    def _run(self):
        """Start calculating a path in the background."""
        self.client.pathfind(
            self.state_tracker.start_state.lines,
            self.state_tracker.start_state.view,
            self.state_tracker.target_state.view,
            self.popup,
        )

    def popup(self, motions):
        self.last_output = motions
        open_popup(output.compact_motions(motions))

    def autorun(self):
        """Called on a timer several times per second."""
        if self.state_tracker.choose_action_using(choose_action) == "pathfind":
            if not cursor_in_same_position(
                self.state_tracker.start_state.view,
                self.state_tracker.target_state.view,
            ):
                self._run()
            self.state_tracker.reset()

    def command_begin(self):
        """Called for the :PathfinderBegin command."""
        self.state_tracker.reset()

    def command_run(self):
        """Called for the :PathfinderRun command."""
        self.state_tracker.set_target()

        if cursor_in_same_position(
            self.state_tracker.start_state.view,
            self.state_tracker.target_state.view,
        ):
            print("You must move the cursor to a new location first!")
        else:
            self._run()

    def command_explain(self):
        """Called for the :PathfinderExplain command."""
        if self.last_output is None:
            print("No suggestion to explain.")
        else:
            # explained_motions yields each line
            # sep tells print to put \n between them rather than space
            print(*output.explained_motions(self.last_output), sep="\n")

    def stop(self):
        """Called when Vim is about to shut down."""
        self.client.close()

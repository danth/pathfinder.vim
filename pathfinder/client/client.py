import os
import subprocess
import tempfile
from multiprocessing import connection

import vim

from pathfinder.client.explore_lines import get_line_limits


class Client:
    """
    Starts and connects to a separate Vim instance used for testing motions.

    This is used to test motions in the exact same environment as the user (loaded via
    a temporary session file), without moving the user's cursor in the process. This
    allows pathfinding to happen in the background while the user may continue working.

    A custom vimrc is used to only load this plugin, disabling other plugins and user
    settings.
    """

    def __init__(self):
        self.open()

    def open(self):
        """Launch and connect to the server Vim."""
        # Create a file used to communicate with the server
        self.file_path = os.path.join(
            tempfile.gettempdir(), "pathfinder_vim_" + vim.eval("getpid()")
        )

        self.server_process = subprocess.Popen(
            self._build_server_cmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        self.server_connection = None
        self.to_send = None

    def _build_server_cmd(self):
        """Build the command used to launch the server Vim."""
        progname = vim.eval("v:progname")  # vim/gvim/nvim etc

        if progname == "nvim":
            python3_host_prog = vim.eval("g:python3_host_prog")
            options = ["--headless", "--cmd", f"let g:python3_host_prog='{python3_host_prog}'"]
        else:
            options = ["-v", "--not-a-term"]

        return (
            [progname]
            + options
            + [
                "--clean",
                "--cmd",
                f"let g:pf_server_communiation_file='{self.file_path}'",
                "-u",
                os.path.normpath(
                    # serverrc.vim in the root of this repository, instead of the user's
                    # regular .vimrc or init.vim
                    os.path.join(os.path.dirname(__file__), "..", "..", "serverrc.vim")
                ),
            ]
        )

    def close(self):
        """Shut down the server Vim."""
        if self.server_connection is not None:
            # Server will shut down Vim gracefully when we disconnect
            self.server_connection.close()
        elif self.server_process is not None:
            # Not connected yet, terminate the process instead
            self.server_process.terminate()

    def poll_responses(self):
        if not self.connect():
            return

        # Check if a request is waiting to be sent
        if self.to_send is not None:
            self.server_connection.send(self.to_send)
            self.to_send = None

        # Check if any data is available to be read
        elif self.server_connection.poll():
            # Get response (sent in a tuple of type, data)
            response_type, data = self.server_connection.recv()
            self.handle_response(response_type, data)

    def connect(self):
        """
        Attempt to connect to the server.

        :returns: whether a connection is ready.
        """
        if self.server_connection is not None:
            return True

        if self.server_process is None:
            # Server process has exited but we already raised an exception
            return False

        return_code = self.server_process.poll()
        if return_code is not None:
            # Server process has exited
            stdout, stderr = self.server_process.communicate()
            self.server_process = None
            raise Exception(
                f"Pathfinding server process exited with return code {return_code}:\n"
                + stderr.decode()
            )

        try:
            # Attempt to connect
            self.server_connection = connection.Client(self.file_path)
            return True
        except FileNotFoundError:
            return False

    def handle_response(self, response_type, data):
        """
        Process a response recieved from the server.

        This will be one of:
        - ``RESULT`` - A pathfinding result. Call the first queued callback.
        - ``ERROR`` - An unexpected exception was caught and the server has exited.
          Relay the traceback to the user for debugging.
        """
        if response_type == "RESULT":
            # Get the first callback function and pass the result to it
            self.callback(data)
            del self.callback
        elif response_type == "ERROR":
            raise Exception("Pathfinding server encountered an exception:\n" + data)
        else:
            raise Exception("Received an unexpected response " + response_type)

    def pathfind(self, buffer_contents, start_view, target_view, callback):
        """
        Request a pathfinding result from the server.

        :param buffer_contents: List of lines we are pathfinding inside.
        :param start_view: The start position, in the current window.
        :param target_view: The target position, in the current window.
        :param callback: Function to be called once a path is found. Recieves a list
            of motions as a parameter.
        """
        self.callback = callback

        min_line, max_line = get_line_limits(start_view, target_view)
        self.to_send = {
            "start": start_view,
            "target": target_view,
            "min_line": min_line,
            "max_line": max_line,
            # Using vim.vars would return a vim.list object which we cannot send
            # because it can't be pickled
            "motions": vim.eval("g:pf_motions"),
            "size": (
                # WindowTextWidth() - see plugin/dimensions.vim
                vim.eval("WindowTextWidth()"),
                vim.eval("winheight(0)"),
            ),
            "buffer": buffer_contents,
            "wrap": vim.current.window.options["wrap"],
            "scrolloff": vim.options["scrolloff"],
        }


client = Client()

import os
import subprocess
import tempfile
from multiprocessing import connection

import vim

from pathfinder.explore_lines import get_line_limits


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

        # serverrc.vim in the root of the repo
        vimrc_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "serverrc.vim")
        )

        # Used to open the server in a console window for development/debugging
        # Set this option to e.g. `konsole -e`
        dev_mode = "pf_dev_server_console" in vim.vars

        vim_cmd = self._build_vim_cmd(vimrc_path, dev_mode)
        self.server_process = subprocess.Popen(vim_cmd)

        self.server_connection = None
        self.to_send = None

    def _build_vim_cmd(self, vimrc_path, dev_mode):
        """
        Build the command used to launch the server Vim.

        :param vimrc_path: Path to serverrc.vim
        :param dev_mode: If True, enable development mode, which opens the server in
            a console (g:pf_dev_server_console) for viewing.
        """
        vim_cmd = list()
        if dev_mode:
            vim_cmd += vim.eval("g:pf_dev_server_console").split(" ")

        progname = vim.eval("v:progname")  # vim/gvim/neovim
        vim_cmd.append(progname)

        if dev_mode:
            # Tell the server that we are in development mode
            vim_cmd += [
                "--cmd",
                "let g:pf_dev_server_console=1",
            ]
        elif progname == "neovim":
            # Disable UI completely
            vim_cmd.append("--headless")
        else:
            # Disable warnings about not being a terminal
            vim_cmd.append("--not-a-term")

        return vim_cmd + [
            "--cmd",
            f"let g:pf_server_communiation_file='{self.file_path}'",
            "-u",
            vimrc_path,
        ]

    def close(self):
        """Shut down the server Vim."""
        if self.server_connection is not None:
            # Server will shut down Vim gracefully when we disconnect
            self.server_connection.close()
        else:
            # Not connected yet, terminate the process instead
            self.server_process.terminate()

    def poll_responses(self):
        if self.server_connection is None:
            # Check if the server has started listening yet
            try:
                self.server_connection = connection.Client(self.file_path)
            except FileNotFoundError:
                # Check status of server process
                return_code = self.server_process.poll()
                if return_code is not None:
                    # Server did not connect because of an error
                    raise Exception(
                        f"Pathfinding server process exited with return code {return_code}"
                    )
                # else: just waiting for server to launch

        # Check if a request is waiting to be sent
        elif self.to_send is not None:
            self.server_connection.send(self.to_send)
            self.to_send = None

        # Check if any data is available to be read
        elif self.server_connection.poll():
            # Get response (sent in a tuple of type, data)
            response_type, data = self.server_connection.recv()
            self.handle_response(response_type, data)

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

    def pathfind(self, start_view, target_view, callback):
        """
        Request a pathfinding result from the server.

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
            "scrolloff": vim.options["scrolloff"],
            "size": (
                # WindowTextWidth() - see plugin/dimensions.vim
                vim.eval("WindowTextWidth()"),
                vim.eval("winheight(0)"),
            ),
            # We don't need to join these lines together, the server expects
            # (and needs) them in list form
            "buffer": vim.eval("getline(0,'$')"),
        }


client = Client()

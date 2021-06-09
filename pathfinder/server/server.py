import traceback
from multiprocessing import connection

import vim

from pathfinder.debytes import debytes
from pathfinder.server.dijkstra import Dijkstra


class Server:
    """
    Local server which runs inside an instance of Vim in a separate process.

    This is used to test motions in the same environment as the user, but without
    blocking their Vim or moving their cursor. This allows pathfinding to happen in
    the background while the user may continue working.

    The server's Vim is quitted as soon as the client (the user's Vim) disconnects,
    which happens when it is closed. It will also exit if an exception is caught,
    relaying the traceback message to the client beforehand so that it can be displayed
    for debugging.
    """

    def __init__(self, file_path):
        self.listener = connection.Listener(debytes(file_path))

    def run(self):
        try:
            # Wait for the user's Vim to connect
            self.client_connection = self.listener.accept()
            # Continuously process jobs until EOFError is raised
            # (when the client disconnects)
            self.message_loop()
        except EOFError:
            pass
        finally:
            self.listener.close()
            # Exit the background Vim since it is no longer needed
            vim.command("qa!")

    def message_loop(self):
        """
        Continuously wait for and handle instructions from the client.

        This waiting blocks Vim, but that does not matter since nobody is looking at
        it. Blocking also prevents CPU resources from being wasted on redrawing.

        :raises EOFError: when the connection is closed.
        """
        while True:
            try:
                data = self.client_connection.recv()

                # If there is still data waiting, then multiple requests were sent,
                # so we skip pathfinding and move on to the next one
                if not self.client_connection.poll():
                    self.do_action(data)
            except:
                # Send any unexpected exceptions back to the client
                # to be displayed for debugging purposes
                self.client_connection.send(("ERROR", traceback.format_exc()))

    def do_action(self, data):
        """Process an instruction from the client."""
        self.start_view = data["start"]
        self.target_view = data["target"]
        self.min_line = data["min_line"]
        self.max_line = data["max_line"]

        vim.current.buffer[:] = data["buffer"]

        vim.current.window.options["wrap"] = data["wrap"]
        vim.options["scrolloff"] = data["scrolloff"]
        vim.options["sidescrolloff"] = data["sidescrolloff"]

        # Set size of the entire Vim display to match the size of the
        # corresponding window in the client
        vim.options["columns"] = int(data["size"][0])
        vim.options["lines"] = vim.options["cmdheight"] + int(data["size"][1])

        self.pathfind()

    def pathfind(self):
        """Run the pathfinder, then send the result back to the client."""
        dijkstra = Dijkstra(
            self.start_view, self.target_view, self.min_line, self.max_line
        )
        motions = dijkstra.find_path(self.client_connection)

        # If motions is None, that means we cancelled pathfinding because a new
        # request was received. We also check for another request now in case one was
        # sent during the last iteration of the pathfinding loop.
        if not (motions is None or self.client_connection.poll()):
            self.client_connection.send(("RESULT", motions))


server = Server(vim.vars["pf_server_communication_file"])
server.run()

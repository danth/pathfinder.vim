import traceback
from multiprocessing import connection

import vim
from pathfinder import Path


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
        self.listener = connection.Listener(file_path.decode())

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
            # Wait for instructions (sent in a tuple of action, data)
            action, data = self.client_connection.recv()

            try:
                self.do_action(action, data)
            except:
                # Send any unexpected exceptions back to the client
                # to be displayed for debugging purposes
                self.client_connection.send(("ERROR", traceback.format_exc()))

    def do_action(self, action, data):
        """
        Process an instruction received from the client.

        This will be one of:
        - ``START`` - Set the start view.
        - ``TARGET`` - Set the target view.
        - ``SIZE`` - Set the window dimensions. This is measured in main Vim using
          winwidth(0) and winheight(0), but restored using &lines and &columns so we
          don't need to create additional windows to get the right size.
        - ``BUFFER`` - Transfer the contents of the current buffer.
        - ``MOTIONS`` - Transfer the value of g:pf_motions.
        - ``SCROLLOFF`` - Transfer the value of &scrolloff (important for H,M,L).
        - ``RUN`` - After all the steps above have happened (in any order), do the
          actual pathfinding and send back a result.
        """
        if action == "START":
            self.start_view = data
        elif action == "TARGET":
            self.target_view = data
        elif action == "SIZE":
            # Set size of the entire Vim display to match the size of the
            # corresponding window in the client
            vim.options["lines"] = vim.options["cmdheight"] + int(data[0])
            vim.options["columns"] = int(data[1])
        elif action == "BUFFER":
            vim.current.buffer[:] = data
        elif action == "MOTIONS":
            vim.vars["pf_motions"] = data
        elif action == "SCROLLOFF":
            vim.options["scrolloff"] = data
        elif action == "RUN":
            self.pathfind()
        else:
            raise Exception(f"Received an unexpected action " + action)

    def pathfind(self):
        """Run the pathfinder, then send the result back to the client."""
        path = Path(self.start_view, self.target_view)
        motions = path.find_path()
        self.client_connection.send(("RESULT", motions))


server = Server(vim.vars["pf_server_communiation_file"])
server.run()

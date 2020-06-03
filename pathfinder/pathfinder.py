import heapq

import vim

from pathfinder.motion import Motion
from pathfinder.node import Node, StartNode
from pathfinder.window import cursor_in_same_position


class Path:
    """A path between a cursor start point and end point."""

    def __init__(self, from_view, target_view):
        self.from_view = from_view
        self.target_view = target_view

        self.available_motions = [Motion(m) for m in vim.vars["pf_motions"]]

    def _update_preexisting_node(self, node, preexisting_node):
        """
        Modify a preexisting node using data from the other given node.

        This is used to update a node with the better path, or add a congruent motion to
        the incoming_motions, when a new child node is found on the same position.

        :param node: Node to get new information from.
        :param preexisting_node: Node to be updated.
        """
        if node is None or preexisting_node.closed:
            return

        if node.g == preexisting_node.g and node.parent == preexisting_node.parent:
            # Same g, add motion as an alternative.
            # Since we don't know what motions are coming in the path ahead,
            # we can't process the tiebreaking (select the motion which can
            # combine with its neighbours to reduce keystrokes) now, so instead
            # that happens in a "refining" stage once the target is reached.
            preexisting_node.incoming_motions.append(node.incoming_motions[0])

        elif node.g < preexisting_node.g:
            # This is a shorter route (lower g), discard the existing node and
            # replace it with this one.
            preexisting_node.__dict__.update(node.__dict__)
            # Maintain heap invariant after this change
            heapq.heapify(self.open_nodes)

    def find_path(self, client_connection, min_line, max_line):
        """
        Use Dijkstra's algorithm to find the optimal sequence of motions.

        :param client_connection: If another pathfinding request is waiting on this
            connection, exit (returning None) as soon as possible. This cancels the
            pathfinding, moving on to the new request immediately.
        :param min_line: Do not explore above this line number.
        :param max_line: Do not explore below this line number.
        """
        # Dictionary of all nodes (both open and closed) indexed by the line and column
        self.nodes = {}
        # Priority queue of open nodes to efficiently find the node with the lowest g
        # (using heapq module)
        self.open_nodes = [StartNode(self.from_view)]

        while len(self.open_nodes) > 0 and not client_connection.poll():
            current_node = heapq.heappop(self.open_nodes)
            current_node.closed = True

            if cursor_in_same_position(current_node.view, self.target_view):
                # We found the target!
                return current_node.get_refined_path()

            # Loop through child nodes of the current node
            for child_node in current_node.child_nodes(
                self.available_motions, min_line, max_line
            ):
                if child_node.key() in self.nodes:
                    preexisting_child_node = self.nodes[child_node.key()]
                    self._update_preexisting_node(child_node, preexisting_child_node)
                else:
                    # Add a new node
                    self.nodes[child_node.key()] = child_node
                    heapq.heappush(self.open_nodes, child_node)

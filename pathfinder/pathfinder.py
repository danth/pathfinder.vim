import math

import vim
from heapdict.heapdict import heapdict

from pathfinder.motion import Motion
from pathfinder.node import Node, StartNode
from pathfinder.window import cursor_in_same_position


class Path:
    """A path between a cursor start point and end point."""

    def __init__(self, from_view, target_view):
        self.from_view = from_view
        self.target_view = target_view

        self.available_motions = [Motion(m) for m in vim.vars["pf_motions"]]

    def find_path(self, client_connection, min_line, max_line):
        """
        Use Dijkstra's algorithm to find the optimal sequence of motions.

        :param client_connection: If another pathfinding request is waiting on this
            connection, exit (returning None) as soon as possible. This cancels the
            pathfinding, moving on to the new request immediately.
        :param min_line: Do not explore above this line number.
        :param max_line: Do not explore below this line number.
        """
        start_node = StartNode(self.from_view)
        # This is a min-priority queue implemented using a heap, but is faster than
        # heapq because it uses a dictionary to allow us to update a node's priority
        # (g) faster.
        open_nodes = heapdict()
        open_nodes[start_node] = 0

        closed_nodes = list()

        while len(open_nodes) > 0 and not client_connection.poll():
            current_node, current_g = open_nodes.popitem()
            closed_nodes.append(current_node)

            if cursor_in_same_position(current_node.view, self.target_view):
                # We found the target!
                return current_node.get_refined_path()

            for child_node, motion in current_node.child_nodes(
                self.available_motions, min_line, max_line
            ):
                if child_node in closed_nodes:
                    continue

                # Get the g value of an identical node which is already in the open set.
                # If one does not exist, default to infinity so that it is added.
                child_g = open_nodes.get(child_node, math.inf)
                # Calculate what g would be for the child node if we reached it via
                # the current node.
                child_new_g = current_g + child_node.weight(motion)

                if child_new_g < child_g:
                    # Reaching the child node through the current node is better.
                    # Either update the existing priority, or add the node to the open
                    # set.
                    open_nodes[child_node] = child_new_g
                elif child_new_g == child_g:
                    # Add this as an alternative path into the child node.
                    child_node.incoming_motions.append(motion)

import math

import vim
from heapdict import heapdict

from pathfinder.motion import motions
from pathfinder.server.child_views import child_views
from pathfinder.server.node import Node, StartNode
from pathfinder.window import cursor_in_same_position


class NodeClosed(Exception):
    """
    Exception raised when trying to update a closed node.
    """

    pass


class Path:
    """A path between a cursor start point and end point."""

    def __init__(self, from_view, target_view):
        self.from_view = from_view
        self.target_view = target_view

        self.available_motions = list(motions())

        # This is a min-priority queue implemented using a heap, but is faster than
        # heapq because it uses a dictionary to allow us to update a node's priority
        # (g) faster.
        self._open_nodes = heapdict()

        # Dictionary of all nodes indexed by view.
        self._nodes = dict()

        self._start_node = StartNode(self.from_view)
        self._add_node(self._start_node, 0)

    def _add_node(self, node, g):
        key = tuple(node.view.values())
        self._nodes[key] = node

        self._open_nodes[node] = g

    def _get_node(self, view):
        key = tuple(view.values())
        return self._nodes[key]

    def _add_connection(self, view, motion):
        """
        Add a connection from self._current_node to the node associated with the given view.

        This will either:
        - Create a new node if one did not already exist
        - Replace the existing route into the node if this motion is better
        - Add this motion as an alternative
        - Do nothing if this motion is worse than the existing route

        :param view: The view (position and scroll details) of the connected node.
        :param motion: Motion used to reach this node.
        """
        try:
            # Look for an existing node with this view
            node = self._get_node(view)
        except KeyError:
            # Not found, initialize a new node
            node = Node(view, self._current_node, motion)
            node_g = self._current_g + node.weight(motion, self._current_node)
            self._add_node(node, node_g)
        else:
            self._update_node(node, motion)

    def _update_node(self, node, motion):
        """
        Update node to use the given motion, only if it is better than the current path.

        :param node: Node to update.
        :param motion: Motion used from self._current_node to reach this node.
        :raises NodeClosed: If the node to update is not in the open set.
        """
        try:
            node_g = self._open_nodes[node]
        except KeyError:
            # The node exists, but is not in the open set, hence it must be closed
            raise NodeClosed()

        # Calculate what g would be if we reached `node` using this motion
        new_node_g = self._current_g + node.weight(motion, self._current_node)
        if new_node_g < node_g:
            # This is a better route into the node
            node.parent = self._current_node
            node.incoming_motions = [motion]
            self._open_nodes[node] = new_node_g
        elif new_node_g == node_g and node.parent == self._current_node:
            # This motion is congruent, add it as an alternative
            node.incoming_motions.append(motion)

    def find_path(self, client_connection, min_line, max_line):
        """
        Use Dijkstra's algorithm to find the optimal sequence of motions.

        :param client_connection: If another pathfinding request is waiting on this
            connection, exit (returning None) as soon as possible. This cancels the
            pathfinding, moving on to the new request immediately.
        :param min_line: Do not explore above this line number.
        :param max_line: Do not explore below this line number.
        """
        while len(self._open_nodes) > 0 and not client_connection.poll():
            self._current_node, self._current_g = self._open_nodes.popitem()

            if cursor_in_same_position(self._current_node.view, self.target_view):
                # We found the target!
                return self._current_node.get_refined_path()

            for motion, child_view in child_views(
                self._current_node, self.available_motions, min_line, max_line
            ):
                try:
                    # Add a connection from self._current_node to the node
                    # associated with the child view.
                    # This will either replace the existing path into the node,
                    # add the motion as an alternative, or create a new node if
                    # one did not already exist.
                    self._add_connection(child_view, motion)
                except NodeClosed:
                    pass

from heapdict import heapdict

from pathfinder.server.node import Node
from pathfinder.motion import motions


class Dijkstra:
    """
    A path between a start and end point in the same window.

    :param from_view: View of the start point
    :param target_view: View of the target point
    :param min_line: Do not explore nodes above this line
    :param max_line: Do not explore nodes below this line
    """

    def __init__(self, from_view, target_view, min_line, max_line):
        self.from_view = from_view
        self.target_view = target_view
        self.min_line = min_line
        self.max_line = max_line

        self.available_motions = list(motions())

        self._open_queue = heapdict()  # Min-priority queue: Key -> Distance
        self._open_nodes = dict()  # Key -> Node
        self._closed_nodes = set()  # Key

        start_node = Node(self, self.from_view, None)
        self._open_queue[start_node.key] = 0
        self._open_nodes[start_node.key] = start_node

    def find_path(self, client_connection):
        """
        Use Dijkstra's algorithm to find the optimal sequence of motions.

        :param client_connection: If another pathfinding request is waiting on this
            connection, exit (returning None) as soon as possible. This cancels the
            pathfinding, moving on to the new request immediately.
        """
        while len(self._open_queue) > 0 and not client_connection.poll():
            current_node_key, current_distance = self._open_queue.popitem()
            current_node = self._open_nodes.pop(current_node_key)
            self._closed_nodes.add(current_node_key)

            if current_node.is_target():
                return current_node.reconstruct_path()

            for node in current_node.get_neighbours():
                if node.key in self._closed_nodes:
                    continue

                new_distance = (current_distance +
                                current_node.motion_weight(node.came_by_motion))
                if (
                    node.key not in self._open_nodes
                    or new_distance < self._open_queue[node.key]
                ):
                    node.set_came_from(current_node)
                    self._open_nodes[node.key] = node
                    self._open_queue[node.key] = new_distance

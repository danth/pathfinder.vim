from collections import namedtuple

from heapdict import heapdict

from pathfinder.motion import motions
from pathfinder.server.child_views import child_views
from pathfinder.window import cursor_in_same_position

# A combination of a cursor location, scroll location, and most recent motion.
# These become the vertices of the pathfinding graph.
State = namedtuple("State", ("view", "motion"))
# Associate a state with a previously-traversed node, and a counter of how many
# times the most recent motion was repeated. We must store the most recent motion
# and the counter because the weight of subsequent repetitions is dependent on
# this (fx -> 2fx is cheaper than fx -> fxfy).
Node = namedtuple("Node", ("state", "parent", "motion_count"))


class Path:
    """A path between a cursor start point and end point."""

    def __init__(self, from_view, target_view):
        self.from_view = from_view
        self.target_view = target_view

        self.available_motions = list(motions())

        self._open_queue = heapdict()  # Min-priority queue: State -> Distance
        self._open_nodes = dict()  # State -> Node
        self._closed_nodes = dict()  # State -> Node

        start_state = State(self.from_view, None)
        self._open_nodes[start_state] = Node(start_state, None, None)
        self._open_queue[start_state] = 0

    def _edge_weight(self, node, state):
        """
        :param node: Parent node.
        :param state: The state we are moving to.
        :returns: Weight of the edge between `node` and `state`.
        """
        if node.state.motion != state.motion:
            # First use of this motion, e.g. gg -> j
            # Use the motion's configured weight
            return state.motion.weight
        elif node.motion_count == 1:
            # Count has been added, e.g. fx -> 2fx
            # Add 1 unit for the extra character
            return 1
        else:
            # Calculate difference in length of the count
            # e.g. 2j -> 3j = 0,  9j -> 10j = 1
            return len(str(node.motion_count - 1)) - len(str(node.motion_count))

    def _motion_count(self, state, parent):
        """
        :param state: State to get .motion_count for.
        :param parent: The node used to reach this state.
        :returns: Correct .motion_count for the node associated with the given state.
        """
        if parent.state.motion == state.motion:
            # The same motion was repeated again, add a repetition
            return parent.motion_count + 1
        else:
            # Changed motions, reset counter to 1
            return 1

    def _process_edge(self, state, parent, new_distance):
        """
        Process an edge between a parent and state.

        If the state is not already associated with a node, create a node for it.
        If the state is associated with a node, but this route is better, replace that
        node with a new one using this improved route.

        :param state: The state to create or update a node for.
        :param parent: The node used to reach this state.
        :param new_distance: The distance (cost) of using this route.
        """
        if state not in self._open_nodes or new_distance < self._open_queue[state]:
            node = Node(state, parent, self._motion_count(state, parent))
            self._open_nodes[state] = node
            self._open_queue[state] = new_distance

    def _backtrack(self, node):
        """
        Walk backwards through the parents of a node.

        :returns: List of motions used to travel from the start node to this node.
        """
        motions = list()
        while node.parent is not None:
            motions.insert(0, node.state.motion)
            node = node.parent
        return motions

    def find_path(self, client_connection, min_line, max_line):
        """
        Use Dijkstra's algorithm to find the optimal sequence of motions.

        :param client_connection: If another pathfinding request is waiting on this
            connection, exit (returning None) as soon as possible. This cancels the
            pathfinding, moving on to the new request immediately.
        :param min_line: Do not explore above this line number.
        :param max_line: Do not explore below this line number.
        """
        while len(self._open_queue) > 0 and not client_connection.poll():
            current_state, current_distance = self._open_queue.popitem()
            current_node = self._open_nodes.pop(current_state)
            self._closed_nodes[current_state] = current_node

            if cursor_in_same_position(current_state.view, self.target_view):
                # We found the target!
                return self._backtrack(current_node)

            for motion, view in child_views(
                current_state.view, self.available_motions, min_line, max_line
            ):
                state = State(view, motion)
                if not state in self._closed_nodes:
                    new_distance = current_distance + self._edge_weight(
                        current_node, state
                    )
                    self._process_edge(state, current_node, new_distance)

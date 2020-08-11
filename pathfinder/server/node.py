from pathfinder.server.child_views import child_views
from pathfinder.window import cursor_in_same_position


class Node:
    """Graph node linked to a view (cursor+scroll location) within the document."""

    def __init__(self, dijkstra, view, came_by_motion):
        self.dijkstra = dijkstra
        self.view = view
        self.came_by_motion = came_by_motion

        self.key = (view, came_by_motion)

        self.came_from = None
        self.came_by_motion_repetitions = 1

    def get_neighbours(self):
        """Yield all neighbours of this node."""
        for motion, view in child_views(
            self.view,
            self.dijkstra.available_motions,
            self.dijkstra.min_line,
            self.dijkstra.max_line,
        ):
            yield Node(self.dijkstra, view, motion)

    def motion_weight(self, motion):
        """Return the weight of using a motion from this node."""
        if motion != self.came_by_motion:
            # First repetition, return number of characters in the motion
            return motion.weight
        elif self.came_by_motion_repetitions == 1:
            # Second repetition, adding a "2" is 1 extra character
            return 1
        else:
            # Difference in length of current and future count
            # 2j -> 3j = 0
            # 9j -> 10j = 1
            return len(str(self.came_by_motion_repetitions + 1)) - len(
                str(self.came_by_motion_repetitions)
            )

    def set_came_from(self, node):
        """Set the node this node was reached from."""
        self.came_from = node

        if node.came_by_motion == self.came_by_motion:
            self.came_by_motion_repetitions = node.came_by_motion_repetitions + 1
        else:
            self.came_by_motion_repetitions = 1

    def is_target(self):
        return cursor_in_same_position(self.view, self.dijkstra.target_view)

    def reconstruct_path(self):
        """Return the sequence of motions used to reach this node."""
        motions = list()
        node = self
        while node.came_from is not None:
            motions.insert(0, node.came_by_motion)
            node = node.came_from
        return motions

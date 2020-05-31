import vim

from window import cursor_in_same_position, winrestview, winsaveview


class StartNode:
    """
    The root pathfinding node.

    :param view: The view representing the position this node is at, obtained from
        winsaveview().
    """
    def __init__(self, view):
        self.view = view
        self.g = 0
        self.closed = False

    def key(self):
        return self.view["lnum"], self.view["col"]

    def test_motion(self, motion):
        """
        Attempt to run the given motion from this node's position within Vim.

        :returns: Newly-created child node, if the motion moved the cursor to another
            position and did not cause an error. Otherwise None.
        """
        winrestview(self.view)
        try:
            vim.command("silent! normal! " + motion.motion)
        except vim.error:
            # Ignore motions which fail
            return

        new_view = winsaveview()
        if not cursor_in_same_position(new_view, self.view):
            # The cursor has moved, return the newly created node
            return Node(new_view, self, motion)

    def __eq__(self, other):
        return self.g == other.g

    def __gt__(self, other):
        return self.g > other.g

    def __lt__(self, other):
        return self.g < other.g

    def __ge__(self, other):
        return self.g >= other.g

    def __le__(self, other):
        return self.g <= other.g


class Node(StartNode):
    """
    A pathfinding node.

    :param view: The view representing the position this node is at, obtained from
        winsaveview().
    :param parent: Parent node.
    :param motion: Initial motion to add to incoming_motions.
    """
    def __init__(self, view, parent, motion):
        self.view = view
        self.parent = parent
        self.incoming_motions = [motion]
        self.closed = False

        self.g = parent.g + self._calculate_g_increment(motion)

    def _calculate_g_increment(self, motion):
        repetitions = 0
        for node in self.backtrack():
            if motion in node.incoming_motions:
                repetitions += 1
            else:
                break

        if repetitions == 1:
            return motion.weight  # First use of this motion, e.g. gg -> j
        elif repetitions == 2:
            return 1  # Count has been added, e.g. j -> 2j
        else:
            # Calculate difference in count lengths, e.g. 2j -> 3j = 0, 9j -> 10j = 1
            return len(str(repetitions)) - len(str(repetitions - 1))

    def backtrack(self):
        """
        Generator which yields each ancestor node.

        Includes this node, excludes the start node.
        """
        node = self
        while isinstance(node, Node):
            yield node
            node = node.parent

    def get_refined_path(self):
        """
        Get the optimal set of motions to reach this node.

        Where a choice is encountered between two congruent motions, try to maximize
        the number of repeated motions (possibly resulting in a shorter final
        representation of the path due to combining with counts).
        """
        # Build a 2d list where each item is the set of choices for that position in
        # the sequence
        # Since backtracking is, well, backwards, we flip it around using [::-1]
        motion_options = [node.incoming_motions
                          for node in self.backtrack()][::-1]

        def best_motion_from_triplet(left, centre, right):
            if len(centre) < 2:
                return centre[0]

            # Find motions we have in common with either side
            left_and_centre = set.intersection(set(left), set(centre))
            centre_and_right = set.intersection(set(centre), set(right))

            if len(left_and_centre) > 0 and len(centre_and_right) > 0:
                # Look for motions we have in common with *both* sides
                both_sides = set.intersection(left_and_centre,
                                              centre_and_right)
                if both_sides:
                    return both_sides.pop()

            if centre_and_right:
                return centre_and_right.pop()
            if left_and_centre:
                return left_and_centre.pop()

            # There are no common motions, just use the first one
            return centre[0]

        # Select the best motions from the available options.
        motions = list()
        for i, centre in enumerate(motion_options):
            left = motion_options[i - 1] if i > 0 else []
            right = motion_options[i +
                                   1] if i < len(motion_options) - 1 else []
            motions.append(best_motion_from_triplet(left, centre, right))

        return motions

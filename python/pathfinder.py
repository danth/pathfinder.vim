import heapq

import vim
from node import Node, StartNode
from window import cursor_in_same_position


class Motion:
    def __init__(self, dict):
        self.motion = dict["motion"].decode()
        self.weight = dict["weight"]
        self.description_template = dict["description"].decode()

    def description(self, count):
        return self.description_template.format(count=count)


def update_preexisting_node(node, preexisting_node, open_nodes):
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
        heapq.heapify(open_nodes)


def find_path(from_view, target_view):
    """
    Use Dijkstra's algorithm to find the optimal path between the two given cursor
    locations.
    """
    available_motions = [Motion(m) for m in vim.vars["pf_motions"]]

    # The start node is a special kind of node which has g=0 and doesn't store a
    # parent or incoming motions
    start_node = StartNode(from_view)

    # Dictionary of all nodes (both open and closed) indexed by the line and column
    nodes = {}
    # Priority queue of open nodes to efficiently find the node with the lowest g
    # (using heapq module)
    open_nodes = [start_node]

    while len(open_nodes) > 0:
        current_node = heapq.heappop(open_nodes)
        current_node.closed = True

        if cursor_in_same_position(current_node.view, target_view):
            # We found the target!
            return current_node.get_refined_path()

        # Loop through child nodes of the current node
        # This is done by looping through the configured motions and testing each one
        for motion in available_motions:
            child_node = current_node.test_motion(motion)
            if child_node is None:
                continue

            if child_node.key() in nodes:
                preexisting_child_node = nodes[child_node.key()]
                update_preexisting_node(child_node, preexisting_child_node, open_nodes)
            else:
                # Add a new node
                nodes[child_node.key()] = child_node
                heapq.heappush(open_nodes, child_node)

    raise Exception("No path found")

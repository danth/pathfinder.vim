def child_views(node, available_motions, min_line, max_line):
    """
    Yield each child view found using the given list of motions.

    This will be in the form (motion, resulting view).

    :param node: Node to find children of.
    :param available_motions: List of motions available for use.
    :param min_line: Results above this line number will be ignored.
    :param max_line: Results below this line number will be ignored.
    """
    for motion in available_motions:
        child_view = node.test_motion(motion)

        if (
            child_view is not None
            and int(child_view["lnum"]) >= min_line
            and int(child_view["lnum"]) <= max_line
        ):
            yield motion, child_view

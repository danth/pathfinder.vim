import vim


def get_explore_lines(search_area_lines):
    """
    :param search_area_lines: Number of lines between, and including, the start and
        target positions.
    :returns: Number of lines to explore either side of the search area.
    """
    # Get setting values from Vim variables
    explore_scale = int(vim.vars["pf_explore_scale"])
    max_explore = int(vim.vars["pf_max_explore"])

    if explore_scale < 0:
        # This filtering is disabled, explore the entire buffer
        return len(vim.current.buffer)

    # Number of lines to explore above and below the search area is scaled based
    # on the length of the area. This setting defaults to 0.5, if the search area
    # was e.g. 6 lines then 3 more lines would be explored on either side.
    explore_lines = search_area_lines * explore_scale
    if max_explore >= 0:
        # Limit to no more than max_explore lines
        return min(max_explore, explore_lines)
    else:
        # Do not limit
        return explore_lines


def get_line_limits(start_view, target_view):
    """
    Return the minimum and maximum line numbers to explore.

    :param start_view: The start position.
    :param target_view: The target position.
    :returns: Tuple of (min line, max line)
    """
    min_line = min(int(start_view["lnum"]), int(target_view["lnum"]))
    max_line = max(int(start_view["lnum"]), int(target_view["lnum"]))
    explore_lines = get_explore_lines(max_line - min_line)

    return (
        max(1, min_line - explore_lines),
        min(len(vim.current.buffer), max_line + explore_lines)
    )


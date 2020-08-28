import re

import vim

from pathfinder.server.motions import Motion, MotionGenerator


class SearchMotionGenerator(MotionGenerator):
    def generate(self, view):
        # Only return results from the starting node
        if view != self.dijkstra.from_view:
            return

        motion = self._search_lines(
            vim.current.buffer[:],
            view.lnum - 1,
            view.col,
            self.dijkstra.target_view.lnum - 1,
            self.dijkstra.target_view.col,
        )
        if motion:
            yield self._create_node(self.dijkstra.target_view, motion)

    def _create_motion(self, search_query, motion="/"):
        return Motion(motion, self._escape_magic(search_query))

    def _escape_magic(self, search_query):
        """Add backslash escapes to any "magic" characters in a query."""
        for char in r"\^$.*[~/":
            search_query = search_query.replace(char, "\\" + char)
        return search_query

    def _search(self, text, start, target):
        """
        Return the simplest possible searching motion to reach the given target.

        :param text: Contents of the file.
        :param start: Index in ``text`` to start the search from.
        :param target: Index of the target position in ``text``.
        """
        search_text = text[target:]

        # ("a", "ab", "abc", "abcd"...) until we reach
        # the end of search_text or find a working query
        for query_length in range(1, len(search_text) + 1):
            query = search_text[:query_length]

            # Get a list of all match positions for this search query
            # query="x" text="x___x_xx" == [0, 4, 6, 7]
            pattern = re.escape(query)
            matches = [m.start() for m in re.finditer(pattern, text)]

            if matches:
                # Sort the list so it begins with matches after `start`, rather
                # than matches at the beginning of the file
                # sorted([True, False]) == [False, True]
                matches.sort(key=lambda position: position <= start)

                if matches[0] == target:
                    return self._create_motion(query)
                if matches[-1] == target:
                    return self._create_motion(query, "?")

    def _search_lines(self, lines, start_line, start_col, target_line, target_col):
        """
        Wrapper around _search which handles 2d coordinates and a list of lines.

        :param lines: List of lines.
        :param start_line: Starting line, indexed from 0.
        :param start_col: Starting column.
        :param target_line: Target line, indexed from 0.
        :param target_col: Target column.
        """
        text = "\n".join(lines)
        start = sum(len(line) + 1 for line in lines[:start_line]) + start_col
        target = sum(len(line) + 1 for line in lines[:target_line]) + target_col
        return self._search(text, start, target)

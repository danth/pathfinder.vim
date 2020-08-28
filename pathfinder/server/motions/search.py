import vim

from pathfinder.server.motions import Motion, MotionGenerator


class SearchMotionGenerator(MotionGenerator):
    def generate(self, view):
        if view != self.dijkstra.from_view:
            return

        search_query = self._search_lines(
            vim.current.buffer[:],
            view.lnum - 1,
            view.col,
            self.dijkstra.target_view.lnum - 1,
            self.dijkstra.target_view.col,
        )
        if search_query is not None:
            motion = Motion("/", self._escape_magic(search_query) + "\")
            yield self._create_node(self.dijkstra.target_view, motion)


    def _escape_magic(self, search_query):
        for char in r"\^$.*[~/":
            search_query = search_query.replace(char, "\\" + char)
        return search_query


    def _search(self, text, start, target):
        search_text = text[target:]

        text = text[start + 1 :] + text[:start]
        target -= start + 1
        if target < 0:
            target = len(text) + target + 1

        for query_length in range(1, len(search_text) + 1):
            query = search_text[:query_length]
            if text.find(query) == target:
                return query


    def _search_lines(self, lines, start_line, start_col, target_line, target_col):
        text = "\n".join(lines)
        start = sum(len(line) + 1 for line in lines[:start_line]) + start_col
        target = sum(len(line) + 1 for line in lines[:target_line]) + target_col
        return self._search(text, start, target)

import vim

from pathfinder.server.motions import Motion, MotionGenerator


class FindMotionGenerator(MotionGenerator):
    MOTIONS = {"f", "t", "F", "T"}

    def generate(self, view):
        for motion in self.MOTIONS:
            yield from self._find(view, motion)

    def _find(self, view, motion):
        line_text = vim.current.buffer[view.lnum - 1]
        seen_characters = set()

        # characters = string of characters which may be accessible using this motion
        # column = lambda function which converts index in `characters` to a column number
        if motion == "f" and view.col < len(line_text):
            column = lambda i: view.col + i + 1
            characters = line_text[view.col + 1 :]
        elif motion == "t" and view.col < len(line_text) - 1:
            column = lambda i: view.col + i + 1
            characters = line_text[view.col + 2 :]
            seen_characters.add(line_text[view.col + 1])
        elif motion == "F" and view.col > 0 and len(line_text) > view.col:
            column = lambda i: view.col - i - 1
            # Characters are reversed because we are looking backwards
            characters = line_text[: view.col][::-1]
        elif motion == "T" and view.col > 1 and len(line_text) > view.col:
            column = lambda i: view.col - i - 1
            characters = line_text[: view.col - 1][::-1]
            seen_characters.add(line_text[view.col - 1])
        else:
            return

        for i, character in enumerate(characters):
            # Only use each unique character once
            if character in seen_characters:
                continue
            seen_characters.add(character)

            new_col = column(i)
            new_view = view._replace(col=new_col, curswant=new_col)
            yield self._create_node(new_view, Motion(motion, character))

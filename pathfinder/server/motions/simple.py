import vim

from pathfinder.window import winsaveview, winrestview
from pathfinder.server.motions import MotionGenerator, Motion


class SimpleMotionGenerator(MotionGenerator):
    MOTIONS = {"h", "j", "k", "l", "gj", "gk", "gg", "G", "H", "M", "L", "",
               "", "", "", "", "", "zt", "z\", "z.", "zb", "z-",
               "0", "^", "g^", "$", "g$", "g_", "gm", "gM", "W", "E", "B",
               "gE", "w", "e", "b", "ge", "(", ")", "{", "}", "]]", "][","[[",
               "[]", "]m", "[m", "]M", "[M", "*", "#", "g*", "g#", "%"}

    def generate(self, view):
        for motion in self.MOTIONS:
            result_view = self._try_motion(view, motion)
            if result_view is not None and result_view != view:
                yield self._create_node(result_view, Motion(motion, None))

    def _try_motion(self, view, motion):
        """
        Use a motion inside Vim, starting from the given view.

        If the motion causes an error, return None.
        """
        winrestview(view)
        try:
            vim.command(f"silent! normal! {motion}")
        except:
            return None
        return winsaveview()

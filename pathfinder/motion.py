from collections import namedtuple

import vim

from pathfinder.debytes import debytes

Motion = namedtuple("Motion", ("motion", "name", "weight", "description_template"))


def motions():
    """Yield each motion in g:pf_motions as a named tuple."""
    for motion in vim.vars["pf_motions"]:
        motion = {debytes(k): debytes(v) for k, v in motion.items()}
        yield Motion(
            motion["motion"],
            motion["name"] if "name" in motion else motion["motion"],
            int(motion["weight"]),
            motion["description"]
        )

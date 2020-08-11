from collections import namedtuple
import abc

from pathfinder.server.node import Node


# motion - The motion such as h,j,k,f,T,gM
# argument - Used for the additional argument to f,t,/ etc
Motion = namedtuple("Motion", "motion argument")


class MotionGenerator(abc.ABC):
    def __init__(self, dijkstra):
        self.dijkstra = dijkstra

    @abc.abstractmethod
    def generate(self, view):
        """Yield all neighbouring nodes found from the given view."""
        pass

    def _create_node(self, *args, **kwargs):
        return Node(self.dijkstra, *args, **kwargs)

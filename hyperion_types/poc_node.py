from typing import *

from hyperion_types.poc import POC
from hyperion_types.target import Target
from hyperion_types.poc_tree_filter import PocTreeFilter


class PocNode(PocTreeFilter):
    def __init__(
            self,
            pocs: List[Type[POC]],
            childs: List['PocNode'],
            layer_filter: Callable[[Target], bool]
    ):
        self.pocs = pocs
        self.childs = childs
        self.layer_filter = layer_filter

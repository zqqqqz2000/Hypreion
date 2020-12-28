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

    def __call__(self, target: Target) -> List[Type[POC]]:
        res: List[Type[POC]] = []
        if self.layer_filter(target):
            res.extend(self.pocs)
        for child in self.childs:
            res.extend(child(target))
        return res

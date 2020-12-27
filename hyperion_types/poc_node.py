from typing import *

from hyperion_types import POC
from hyperion_types.poc_tree_filter import PocTreeFilter


class PocNode(PocTreeFilter):
    def __init__(
            self,
            pocs: List[POC],
            childs: List['PocNode']
    ):
        self.pocs = pocs
        self.childs = childs

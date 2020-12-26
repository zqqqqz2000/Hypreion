from typing import *
from hyperion_types.target import Target
from hyperion_types.poc_tree_filter import PocTreeFilter


class POC(PocTreeFilter):
    """
    The base class of all the POC
    """

    def __init__(self, target: Target):
        self.g = self.execute(target)
        self.target: Target = target

    def execute(self, target: Target):
        raise

    def error_handler(self, error: Exception):
        ...

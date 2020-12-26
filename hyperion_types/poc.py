from typing import *
from core import global_var
from hyperion_types.target import Target
from hyperion_types.poc_tree_filter import PocTreeFilter


class POC(PocTreeFilter):
    """
    The base class of all the POC
    """

    def __init__(self, target: Target):
        self.g = self.execute(target)
        self.target: Target = target
        self.logger = global_var.logger

    def execute(self, target: Target):
        """
        poc main function, should be a generator
        """
        raise

    def error_handler(self, error: Exception):
        """
        when the poc execute with an error, the error information will send to this function and handle
        """
        ...

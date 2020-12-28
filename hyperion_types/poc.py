from typing import *
from core.core_types import Config
from hyperion_types.target import Target
from hyperion_types.poc_tree_filter import PocTreeFilter


class POC(PocTreeFilter):
    """
    The base class of all the POC
    """

    def __init__(self, target: Target, config: Type[Config]):
        self.target: Target = target
        self.g = self.execute()
        self.logger = config.LOGGER

    def execute(self):
        """
        poc main function, should be a generator
        """
        raise

    @staticmethod
    def is_error(res: Union[Dict, Exception]) -> bool:
        return issubclass(type(res), Exception)

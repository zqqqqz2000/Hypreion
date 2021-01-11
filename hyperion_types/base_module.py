import argparse
from typing import *


class BaseModule:
    module_name = 'Base'
    help = 'None'

    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser) -> NoReturn:
        """
        this function will be call when this module be loaded
        and use to inject arguments to argparse
        :param parser: parser of this module
        """
        ...

    @staticmethod
    def execute(args: argparse.Namespace) -> NoReturn:
        """
        the action when this module be execute
        :param args: parser_inner arguments in 'arg_declare'
        """
        ...

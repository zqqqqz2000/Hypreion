import argparse
from typing import *


class BaseModule:
    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser) -> NoReturn:
        """
        this function will be call when this module be loaded
        and use to inject arguments to argparse
        """
        ...

    @staticmethod
    def hit(args: argparse.Namespace) -> bool:
        """
        to determine whether this module be use by user based on args
        """
        ...

    @staticmethod
    def execute(args: argparse.Namespace) -> NoReturn:
        """
        the action when this module be execute
        """
        ...


class NormalModule(BaseModule):
    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            help="load targets from file",
            default=""
        )

        parser.add_argument(
            "-t",
            "--target",
            type=str,
            help="input target directly",
            default=""
        )

        parser.add_argument(
            "--cookies",
            type=str,
            help="cookies of targets, if load from file, this would be a json {'domain': 'cookies'}"
        )

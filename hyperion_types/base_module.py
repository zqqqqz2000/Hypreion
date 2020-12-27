import argparse


class BaseModule:
    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        ...

    @staticmethod
    def hit(args: argparse.Namespace) -> bool:
        ...

    @staticmethod
    def execute(args: argparse.Namespace):
        ...

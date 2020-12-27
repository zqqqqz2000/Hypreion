import argparse
from core import global_var
from core.poc_handler import build_poc_tree
from hyperion_types import BaseModule


class PocAll(BaseModule):
    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        parser.add_argument("-a", "--all", help="test all poc to target", action="store_true")

    @staticmethod
    def hit(args: argparse.Namespace) -> bool:
        return args.all

    @staticmethod
    def execute(args: argparse.Namespace):
        print(3223)
        root, all_pocs = build_poc_tree(global_var.config.POC_BASE_DIR)
        print(all_pocs)

import argparse
from core import global_var
from core.poc_handler import build_poc_tree
from core.requester import mount2dispatcher
from core.requester.requester_types import PocGenerator
from hyperion_types import BaseModule, Target


class PocAll(BaseModule):
    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        parser.add_argument("-a", "--all", help="test all poc to target", action="store_true")

    @staticmethod
    def hit(args: argparse.Namespace) -> bool:
        return args.all

    @staticmethod
    def execute(args: argparse.Namespace):
        root, all_pocs = build_poc_tree(global_var.config.POC_BASE_DIR)
        for poc in all_pocs:
            target = Target('https://www.baidu.com/')
            p = poc(target, global_var.config)
            g = PocGenerator(p)
            mount2dispatcher(g)

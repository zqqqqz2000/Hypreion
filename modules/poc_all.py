import argparse
from core import global_var
from core.poc_handler import build_poc_tree
from core.requester import mount2dispatcher
from core.requester.requester_types import Domain
from hyperion_types import Target, NormalModule


def bounce(res, domain: Domain):
    domain.interval = 1


class PocAll(NormalModule):
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
            mount2dispatcher(p, bounce)

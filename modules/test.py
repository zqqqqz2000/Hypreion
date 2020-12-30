import argparse
from core import global_var
from core.poc_handler import build_poc_tree
from core.requester import mount2dispatcher, Domain, set_domain_config
from hyperion_types import Target, NormalModule, POC
from typing import *


def bounce(res, domain: Domain):
    set_domain_config(domain, interval=1)
    print(f'bounce function called, delayed {domain.interval} s')


def poc_callback(res: Union[POC, Generator, Exception]):
    if POC.is_error(res):
        print(f'error test in callback: {res}')
    else:
        print(f'(callback) poc {res} test done')


class PocAll(NormalModule):
    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        parser.add_argument("--test", help="test all poc to target", action="store_true")

    @staticmethod
    def hit(args: argparse.Namespace) -> bool:
        return args.test

    @staticmethod
    def execute(args: argparse.Namespace):
        root, all_pocs = build_poc_tree(global_var.config.POC_BASE_DIR)
        for poc in all_pocs:
            target = Target('https://www.baidu.com/')
            p = poc(target, global_var.config)
            mount2dispatcher(p, bounce, poc_callback)

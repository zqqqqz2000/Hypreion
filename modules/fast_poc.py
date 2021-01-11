#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   fast_poc.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2021 ICCD

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/1/11 20:53   ICCD       1.0         None
"""
import argparse
from typing import *

from core import global_var
from core.core_types import Logger
from core.modules_handler import load_modules
from core.poc_handler import build_poc_tree
from core.requester import mount2dispatcher, Domain
from hyperion_types import BaseModule, Target


def poc_callback(raw: Any, result: Any):
    print(raw, result)


def bounce(res: Dict, domain: Domain):
    ...


class FastPoc(BaseModule):
    module_name = 'fast'
    help = 'fast test all poc to all target'

    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        parser.add_argument("-t", "--target", help="single target")
        parser.add_argument("-l", "--log", help="specify logger, can be echo")

    @staticmethod
    def execute(args: argparse.Namespace):
        loggers: List[Type[Logger]] = load_modules('logger', Logger)
        for logger in loggers:
            if logger.__name__ == args.log:
                global_var.config.LOGGER = logger
        root, all_pocs = build_poc_tree(global_var.config.POC_BASE_DIR)
        target = Target(args.target)
        fit_pocs = root(target)
        for poc in fit_pocs:
            p = poc(target, global_var.config)
            mount2dispatcher(p, bounce, poc_callback)

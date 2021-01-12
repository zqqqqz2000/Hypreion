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
from crawler.check_cms import CheckCms
from hyperion_types import BaseModule, Target, Crawler, POC


class FastPoc(BaseModule):
    module_name = 'fast'
    help = 'fast test all poc to all target'

    @staticmethod
    def poc_callback(raw: Any, result: Any):
        print(raw, result)

    @staticmethod
    def crawler_callback_pack(root, config):
        def crawler_callback(raw: Any, result: Any):
            fit_pocs: List[Type[POC]] = root(result)
            for poc in fit_pocs:
                mount2dispatcher(poc(result, config), FastPoc.bounce, FastPoc.poc_callback)
            if not result.eval_pocs:
                result.eval_pocs = fit_pocs
            else:
                result.eval_pocs.extend(fit_pocs)

        return crawler_callback

    @staticmethod
    def bounce(res: Dict, domain: Domain):
        ...

    @staticmethod
    def arg_declare(parser: argparse.ArgumentParser):
        parser.add_argument("-t", "--target", help="single target")
        parser.add_argument("-l", "--log", help="specify logger, can be echo")

    @staticmethod
    def execute(args: argparse.Namespace):
        # load logger
        loggers: List[Type[Logger]] = load_modules('logger', Logger)
        for logger in loggers:
            if logger.__name__ == args.log:
                global_var.config.LOGGER = logger

        # load poc tree
        root, all_pocs = build_poc_tree(global_var.config.POC_BASE_DIR)

        # load crawler
        crawlers = load_modules('crawler', Crawler)

        # init target
        target = Target(args.target)

        # start scan
        for crawler in crawlers:
            mount2dispatcher(
                crawler(target, config=global_var.config),
                FastPoc.bounce,
                FastPoc.crawler_callback_pack(root, global_var.config)
            )

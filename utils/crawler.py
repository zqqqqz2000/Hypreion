#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   crawler.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2021 ICCD

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/1/12 19:25   ICCD       1.0         None
"""
from core.requester import requests, mount2dispatcher, Domain
from hyperion_types import Target, PocNode, POC
from bs4 import BeautifulSoup
from typing import *


def first_request(target: Target) -> NoReturn:
    """
    send a request(get and post) to target and save it to pages and htmls of target
    this function cant be execute alone, must yield in generator and used by dispatcher
    :param target: target to test
    :return: None
    """
    if not target.pages:
        page_get = yield requests(target.url)
        page_post = yield requests(target.url, 'post')
        target.pages = [page for page in [page_get, page_post] if page['status'] == 200]

    if not target.htmls:
        target.htmls = []
        for page in target.pages:
            target.htmls.append(BeautifulSoup(page['read'], 'lxml'))


def crawler_callback_find_poc_eval_poc_gen(
        root: PocNode,
        config,
        bounce_function: Callable[[Dict, Domain], NoReturn],
        poc_callback: Callable[[Union[POC, Generator, None], Any], NoReturn]
) -> Callable[[Any, Target], NoReturn]:
    """
    generate a callback function for crawler
    this callback function will get all fit but not been executed poc and execute them
    :param root: the root of poc tree
    :param config: the config of all poc to eval
    :param bounce_function: bounce function of poc
    :param poc_callback: callback when poc eval complete
    :return: use parameters to construct a call back for crawler
    """
    def crawler_callback(raw: Any, result: Target):
        fit_pocs: List[Type[POC]] = root(result)
        for poc in fit_pocs:
            if poc not in result.eval_pocs:
                result.eval_pocs.add(poc)
                mount2dispatcher(poc(result, config), bounce_function, poc_callback)
    return crawler_callback

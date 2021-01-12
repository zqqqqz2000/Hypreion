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
from core.requester import requests
from hyperion_types import Target
from bs4 import BeautifulSoup


def first_request(target: Target):
    if not target.pages:
        page_get = yield requests(target.url)
        page_post = yield requests(target.url, 'post')
        target.pages = [page for page in [page_get, page_post] if page['status'] == 200]

    if not target.htmls:
        target.htmls = []
        for page in target.pages:
            target.htmls.append(BeautifulSoup(page['read'], 'lxml'))

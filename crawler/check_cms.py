#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   check_cms.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2021 ICCD

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/1/12 17:52   ICCD       1.0         None
"""
from hyperion_types import Crawler
from utils.crawler import first_request


class CheckCms(Crawler):
    def execute(self):
        yield first_request(self.target)
        cms = set()
        for html in self.target.htmls:
            title = html.find('title')
            if title:
                if 'BIG-IP' in title.text:
                    cms.add('BIG-IP')
        if cms:
            self.target.cms = cms
        else:
            self.target.cms = 'unknown'
        yield self.target

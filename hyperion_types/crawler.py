#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   crawler.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2021 ICCD

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/1/12 18:50   ICCD       1.0         None
"""
from hyperion_types.poc import POC


class Crawler(POC):
    def execute(self):
        raise self.target

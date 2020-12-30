from typing import *
import re

import aiohttp

from utils.utils import obj2dict


class Request:
    def __init__(
            self, url: str,
            method: str = 'get',
            parameter: Optional[Dict] = None,
            data: Optional[Dict] = None,
            json: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            cookies: Optional[Dict] = None,
            proxy: Optional[str] = None,
            timeout: Optional[float] = None
    ):
        # int
        self.url: str = url
        self.method: str = method
        self.parameter: Optional[Dict] = parameter
        self.data: Optional[Dict] = data
        self.json: Optional[Dict] = json
        self.headers: Optional[Dict] = headers
        self.cookies: Optional[Dict] = cookies
        self.proxy: Optional[str] = proxy
        if timeout is not None:
            self.timeout: Optional = aiohttp.ClientTimeout(total=timeout, connect=None,
                                                           sock_connect=None, sock_read=None)
        else:
            self.timeout: Optional[aiohttp.ClientTimeout] = timeout

    def get_domain(self) -> str:
        url_comp = re.compile(r'[a-zA-Z]+://[^\s]*[.com|.cn]')
        res = url_comp.findall(self.url)
        return res[0]

    def get_aiohttp_parameters(self) -> Dict:
        # attributes in this instance to a dict
        parameters2dict_keys = ['url', 'parameter', 'data', 'json', 'headers', 'cookies', 'proxy', 'timeout']
        return obj2dict(self, parameters2dict_keys, lambda x: x is not None)

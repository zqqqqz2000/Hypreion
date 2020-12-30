from core.requester.dispatcher import Dispatcher
from core.requester.requester_types import Domain
from core.requester.requester_types import Request
from typing import *


def requests(url, method: str = 'get', **kwargs) -> Request:
    r = Request(url, method, **kwargs)
    return r


def set_domain_config(domain: Domain, **configs) -> NoReturn:
    """
    set config of a domain, which will affect request
    :param domain: Domain object
    :param configs: configs include "proxy, interval, cookies, timeout"
    """
    for config in configs:
        if hasattr(domain, config):
            domain.__setattr__(config, configs[config])
    d = Dispatcher()
    d.domains_config.update(configs)

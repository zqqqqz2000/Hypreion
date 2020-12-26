from typing import *

from utils.utils import obj2dict


async def aio_request2dict(request) -> Dict:
    aiohttp_attributes = ['url', 'json', 'read', 'content', 'text', 'headers', 'raw_headers', 'status']
    d = obj2dict(request, aiohttp_attributes, lambda x: True)
    res_dict = {}
    for key, value in d.items():
        if callable(value):
            try:
                res_dict[key] = await value()
            except Exception as Ignore:
                ...
        else:
            res_dict[key] = value
    return res_dict

from core.requester.requester_types.request import Request


def requests(url, method: str = 'get', **kwargs):
    r = Request(url, method, **kwargs)
    return r

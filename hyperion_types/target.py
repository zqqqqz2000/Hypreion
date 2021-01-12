import re

from core.core_errors.target_errors import TargetError


class Target:
    def __init__(self, url: str):
        self.url = url
        self.get_domain()

    def __getattr__(self, item):
        if '_attr_' + item in dir(self):
            return object.__getattribute__(self, '_attr_' + item)
        else:
            return None

    def __setattr__(self, key, value):
        object.__setattr__(self, '_attr_' + key, value)

    def get_domain(self) -> str:
        url_comp = re.compile('^(https?://[^/]*?)(/.*)?$')
        res = url_comp.findall(self.url)
        if not len(res):
            raise TargetError('url not legal, please ensure http or https')
        return res[0]

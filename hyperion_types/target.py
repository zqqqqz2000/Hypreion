import re


class Target:
    def __init__(self, url: str):
        self.url = url

    def __getattr__(self, item):
        if hasattr(self, item):
            return self.__getattribute__(item)
        else:
            return None

    def get_domain(self) -> str:
        url_comp = re.compile('https?://(.*?)/?')
        res = url_comp.findall(self.url)
        return res[0]

from core.requester import requests
from core.requester import mount2dispatcher
from core.requester.requester_types import PocGenerator
from hyperion_types import POC
from hyperion_types.target import Target
import time


class Test(POC):
    def execute(self, target: Target):
        t = time.time()
        for i in range(10):
            res = yield requests(target.url)
            print(res['status'])
        print(time.time() - t)
        yield

    def error_handler(self, error: Exception):
        print(error)

    @staticmethod
    def filter(target: Target):
        return True


if __name__ == '__main__':
    for i in range(100):
        target = Target('https://www.huya.com1/')
        poc = Test(target)
        g = PocGenerator(poc)
        mount2dispatcher(g)

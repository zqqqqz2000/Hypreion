from config import Default
from core.requester import requests
from core.requester import mount2dispatcher
from core.requester.requester_types import PocGenerator
from hyperion_types import POC
from hyperion_types.target import Target
import time


class Test(POC):
    def execute(self):
        t = time.time()
        for i in range(10):
            res = yield requests(self.target.url, timeout=1)
            self.logger.information('Test', res['status'])
        self.logger.information('test', str(time.time() - t))
        yield

    def error_handler(self, error: Exception):
        self.logger.error('test', repr(error))

    @staticmethod
    def filter(target: Target):
        return True


if __name__ == '__main__':
    for i in range(100):
        time.sleep(0.5)
        target = Target('https://www.baidu.com/')
        poc = Test(target, Default())
        g = PocGenerator(poc)
        mount2dispatcher(g)

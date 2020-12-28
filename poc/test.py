import asyncio
from config import Default
from core.requester import requests
from core.requester import mount2dispatcher
from hyperion_types import POC
from hyperion_types.target import Target
import time


async def sleep_return_test():
    await asyncio.sleep(3)
    return 'return success'


class Test(POC):
    def execute(self):
        t = time.time()
        for i in range(10):
            if i >= 5:
                # test error
                self.logger.debug('Test', 'Test error')
                url = '1' + self.target.url
            else:
                # test normal request
                self.logger.debug('Test', 'Test normal request')
                url = self.target.url
            res = yield requests(url, timeout=1)
            if POC.is_error(res):
                self.logger.error('Test', repr(res))
            else:
                self.logger.information('Test', f"status: {res['status']}")
        self.logger.information('test', str(time.time() - t))
        self.logger.debug('Test', 'Test asyncio sleep')
        for i in range(5):
            t = time.time()
            async_result = yield sleep_return_test()
            self.logger.information('Test', async_result + f' sleep {time.time() - t} s')
        self.logger.debug('Test', 'Test done')
        yield

    @staticmethod
    def filter(target: Target):
        return True


if __name__ == '__main__':
    for i in range(100):
        target = Target('https://www.baidu.com/')
        poc = Test(target, Default)
        mount2dispatcher(poc)

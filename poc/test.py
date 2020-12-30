import asyncio
from config import Default
from core.requester import requests
from core.requester import mount2dispatcher
from hyperion_types import POC
from hyperion_types.target import Target
import time


# 测试自定义协程的执行
async def sleep_return_test():
    await asyncio.sleep(3)
    return 'return success'


# 测试自定义的发起request请求的函数
def test_request_inner_function():
    res = yield requests('https://www.baidu.com/', timeout=1)
    yield (res['status'],)


class Test(POC):
    # POC测试主体
    def execute(self):
        t = time.time()
        # 使用模块要求的logger输出
        self.logger.debug('Test', 'Test error')
        res = yield requests('https://111www.baiduuu.com/', timeout=1)
        # 错误捕获
        if POC.is_error(res):
            # 错误则输出错误
            self.logger.error('Test', repr(res))
        else:
            # 正常执行则输出
            self.logger.information('Test', f"status: {res['status']}")
        # 正常访问测试
        self.logger.debug('Test', 'Test normal request')
        res = yield requests('https://www.baidu.com/', timeout=1)
        # 错误捕获
        if POC.is_error(res):
            # 错误则输出错误
            self.logger.error('Test', repr(res))
        else:
            # 正常执行则输出
            self.logger.information('Test', f"status: {res['status']}")
        self.logger.information('Test', str(time.time() - t))
        self.logger.debug('Test', 'Test asyncio sleep')
        # 测试自定的协程
        t = time.time()
        async_result = yield sleep_return_test()
        self.logger.information('Test', async_result + f' sleep {time.time() - t} s')
        self.logger.debug('Test', 'Test done')
        # 测试自定义的发起请求的函数
        res = yield test_request_inner_function()
        print(*res)
        # 重要，请务必使用yield标记POC主体的退出
        yield ('测试完毕',)

    @staticmethod
    def filter(target: Target):
        return True


# 为了确保poc能直接运行，编写main函数，main函数的具体含义在modules中给出
# 逻辑与POC编写无关，此处可以不做理解
if __name__ == '__main__':
    for i in range(100):
        target = Target('https://www.baidu.com/')
        poc = Test(target, Default)
        mount2dispatcher(poc)

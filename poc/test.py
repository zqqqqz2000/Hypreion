from core.requester import requests
import requests as requests_
from core.requester import mount2dispatcher
import time


def poc(target: str):
    t = time.time()
    for i in range(10):
        res = yield requests(target)
        print(res['status'])
    print(time.time() - t)
    yield


def requests_test(target: str):
    t = time.time()
    for i in range(100):
        r = requests_.get(target)
        r.close()
    print(time.time() - t)


if __name__ == '__main__':
    for i in range(100):
        g = poc('https://www.huya.com/')
        mount2dispatcher(g)

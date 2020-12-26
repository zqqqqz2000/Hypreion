import aiohttp
from asyncio import sleep
from typing import *
import time
from utils.aiohttp_operate import aio_request2dict
from utils.utils import do_nothing
from .request import Request


class Domain:
    def __init__(self, domain: str):
        self.headers: Optional[Dict] = None
        self.interval: int = 0
        self.cookies: Optional[Dict] = None
        self.timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=300)
        self.domain: str = domain
        self.last_active_time = time.time()
        # function which control request interval
        self.bounce_function = do_nothing

    async def request(self, request: Request) -> Dict:
        # sleep interval time
        sleep_time = self.interval - (time.time() - self.last_active_time)
        await sleep(max(sleep_time, 0))
        self.last_active_time = time.time()
        parameters = request.get_aiohttp_parameters()
        if 'headers' not in parameters and self.headers is not None:
            parameters['headers'] = self.headers
        if 'cookies' not in parameters and self.cookies is not None:
            parameters['cookies'] = self.cookies
        # call aiohttp request function
        async with aiohttp.ClientSession(
                cookies=self.cookies or {},
                timeout=self.timeout,
                connector=aiohttp.TCPConnector(limit=100)
        ) as session:
            async with session.__getattribute__(request.method)(**parameters) as r:
                # request to dict
                req_dict = await aio_request2dict(r)
        self.bounce_function(req_dict)
        return req_dict

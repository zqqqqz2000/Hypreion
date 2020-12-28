import asyncio
import threading
import time
from asyncio import sleep, coroutine
from config import Default
from typing import *
from core.requester.requester_types.domain import Domain
from core.requester.requester_types.request import Request
from core.core_types import Singleton
from hyperion_types import POC
from utils.utils import do_nothing
from .requester_types import PackedGenerator


class Dispatcher(Singleton):
    """
    Dispatcher is an singleton object which dispatch all the requests.
    When request function called, Dispatcher will get the detail of it (e.g url, cookies, methods)
    and it will pack it into an task_helper coroutine, after the response back, the running stream will give back.
    """
    _first_init_flag = True
    _serve_flag = False
    _t: Optional[threading.Thread] = None
    _loop: asyncio.BaseEventLoop = asyncio.get_event_loop()

    def __init__(self, *args, **kwargs):
        # first init the instance
        if Dispatcher._first_init_flag:
            self.request_pool: List[Tuple[PackedGenerator, Union[Request, asyncio.coroutine]]] = []
            self.domain_pool: Dict[str, Domain] = {}
            self.bounce_func_pool: Dict[str, Callable[[Dict, Domain]]] = {}
            Dispatcher._t = self.start_serve()

    def start_serve(self):
        """
        This function controls the whole dispatcher serve
        :return: None
        """

        async def _task_helper(request_task: coroutine, generator: PackedGenerator):
            """
            All requests will pack to this task_helper coroutine and result will send to generator to get next request
            :param request_task:
            :param generator:
            :return: None
            """
            try:
                res = await request_task
            except Exception as error:
                r = generator.send(error)
            else:
                r = generator.send(res)
            if r:
                self.request_pool.append((generator, r))

        async def _serve_helper():
            """
            Thread and tasks control here
            :return: None
            """
            while Dispatcher._serve_flag:
                # trigger domain clear
                if len(self.domain_pool) > 10000:
                    self._domain_clear()
                tasks = []
                # request with domain instance
                while len(self.request_pool) and Dispatcher._serve_flag:
                    g, request = self.request_pool.pop()
                    if asyncio.iscoroutine(request):
                        tasks.append(_task_helper(request, g))
                        continue
                    domain = request.get_domain()
                    if domain in self.domain_pool:
                        ...
                    else:
                        self.domain_pool[domain] = Domain(domain)
                        if domain in self.bounce_func_pool:
                            self.domain_pool[domain].bounce_function = self.bounce_func_pool[domain]
                    request_task = self.domain_pool[domain].request(request)
                    tasks.append(_task_helper(request_task, g))
                if tasks:
                    await asyncio.wait(tasks)
                else:
                    await sleep(0.001)

        def _async_helper():
            """
            Pack and run asyncio loop to a function, so that the thread can handle it
            :return: None
            """
            Dispatcher._loop.run_until_complete(_serve_helper())

        Dispatcher._serve_flag = True
        # serve thread
        t = threading.Thread(target=_async_helper)
        t.start()
        Dispatcher._t = t
        return t

    @staticmethod
    def stop_serve():
        """
        To stop serve
        if serve stopped, all the tasks which control by dispatcher will pause
        :return: None
        """
        if Dispatcher._serve_flag:
            Dispatcher._serve_flag = False
            Dispatcher._t.join()

    def _domain_clear(self):
        """
        after the domain is inactive, it will be cleared
        :return:
        """
        for domain_name, domain in self.domain_pool.items():
            if time.time() - domain.last_active_time > Default.DOMAIN_SESSION_CLEAR_THRESHOLD:
                del self.domain_pool[domain_name]

    def block(self):
        """
        Block whole thread which call this function until service stop
        :return: None
        """
        self._t.join()


def mount2dispatcher(request_generator: Union[POC, Generator],
                     bounce_function: Callable[[Dict, Domain], Any] = do_nothing):
    """
    Mount a task to Dispatcher
    If dispatcher have no instance, it will create it automaticly and start serve.
    :param request_generator: a task, must be poc or generator, each request yield a Request object.
    :param bounce_function: a function ,which controls the delay of every request on this domain
    :return: None
    """
    if isinstance(request_generator, POC):
        g = request_generator.g
    else:
        g = request_generator
    pg = PackedGenerator(g)
    r = pg.send(None)
    if r is None:
        return
    dispatcher = Dispatcher()
    # load the generator into dispatcher to run
    dispatcher.bounce_func_pool[request_generator.target.get_domain()] = bounce_function
    dispatcher.request_pool.append((g, r))

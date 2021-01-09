#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ${NAME}.py
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2021 ICCD

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
${DATE} ${TIME}   ICCD       1.0         task dispatcher

serve helper:
    if normal return:
        mount2dispatcher
    elif request or coroutine:
        task_helper
    elif generator:
        mount2dispatcher
"""
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
    _serve_flag = False
    _t: Optional[threading.Thread] = None
    _loop: asyncio.BaseEventLoop = asyncio.get_event_loop()

    def __init__(self, *args, **kwargs):
        # first init the instance
        if Dispatcher._first_init_flag:
            # all requests will push to this pool
            self.request_pool: List[Tuple[PackedGenerator, Union[Request, asyncio.coroutine, Generator]]] = []
            # all domains which request recent
            self.domain_pool: Dict[str, Domain] = {}
            # domain config cache
            self.domains_config: Dict[str, Dict] = {}
            # bounce function of all domain
            self.bounce_func_pool: Dict[str, Callable[[Dict, Domain]]] = {}
            self.start_serve()

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
                res = error
            finally:
                try:
                    # send res or error back
                    r = generator.send(res)
                except Exception as error:
                    # if send error, then call generator callback
                    generator.callback(None, error)
                    return
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
                    # if is generator, means the exec flow in a func calling
                    if isinstance(request, Generator):
                        # packing to mount2dispatcher function and callback is inner_func_callback
                        mount2dispatcher(request, callback=inner_func_callback_gen(g))
                        continue
                    # if is coroutine object, just add to task
                    elif asyncio.iscoroutine(request):
                        tasks.append(_task_helper(request, g))
                        continue
                    elif isinstance(request, Request):
                        # is normal request
                        domain = request.get_domain()
                        # check if domain in domain pool
                        if domain in self.domain_pool:
                            domain_obj = self.domain_pool[domain]
                        else:
                            # create domain if not
                            # init domain
                            domain_obj = Domain(domain)
                            self.domain_pool[domain] = domain_obj
                            if domain in self.domains_config:
                                for config in self.domains_config[domain]:
                                    if hasattr(domain_obj, config):
                                        domain_obj.__setattr__(config, self.domains_config[config])
                            if domain in self.bounce_func_pool:
                                domain_obj.bounce_function = self.bounce_func_pool[domain]
                        request_task = domain_obj.request(request)
                        tasks.append(_task_helper(request_task, g))
                    else:
                        # else is normal return
                        mount2dispatcher(g.raw, first_send=request, callback=g.callback)
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

    @classmethod
    def stop_serve(cls):
        """
        To stop serve
        if serve stopped, all the tasks which control by dispatcher will pause
        :return: None
        """
        if cls._serve_flag:
            cls._serve_flag = False
            cls._t.join()

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


def mount2dispatcher(
        request_generator: Union[POC, Generator],
        bounce_function: Callable[[Dict, Domain], Any] = do_nothing,
        callback: Callable[[Union[POC, Generator, Exception], Any], NoReturn] = do_nothing,
        first_send: Any = None
):
    """
    Mount a task to Dispatcher
    If dispatcher have no instance, it will create it automaticly and start serve.
    :param request_generator: a task, must be poc or generator, each request yield a Request object or generator.
    :param bounce_function: a function ,which controls the delay of every request on this domain
    :param callback: a function, will call on request_generator stop StopIteration
    :param first_send: first value send to generator
    :return: None
    """
    if isinstance(request_generator, POC):
        g = request_generator.g
    else:
        g = request_generator
    pg = PackedGenerator(g, callback)
    # save the raw_request_generator
    pg.raw = request_generator
    try:
        r: Optional[Union[Tuple, Request]] = pg.send(first_send)
    except StopIteration as _:
        pg.callback(request_generator, first_send)
        return
    except Exception as error:
        # if send error, then callback
        pg.callback(None, error)
        return
    dispatcher = Dispatcher()
    # load the generator into dispatcher to run
    if isinstance(r, Request):
        # is request
        domain = r.get_domain()
        if not (domain in dispatcher.bounce_func_pool and bounce_function == do_nothing):
            dispatcher.bounce_func_pool[domain] = bounce_function
        dispatcher.request_pool.append((pg, r))
        return
    elif isinstance(r, Generator):
        mount2dispatcher(r, callback=inner_func_callback_gen(pg))
        return
    else:
        # is return value
        callback(pg.raw, r)
        return


def inner_func_callback_gen(parent: PackedGenerator):
    """
    generate a inner function, which will be the callback of 'function called in another function'
    which will mount its parent and result to mount2dispatcher function
    """

    def inner_func_callback(_, res: Any):
        if not isinstance(res, Generator):
            # if call done, return parent
            mount2dispatcher(parent.raw, first_send=res, callback=parent.callback)
        else:
            # inner function call
            mount2dispatcher(parent.raw, first_send=res, callback=inner_func_callback_gen(parent))

    return inner_func_callback

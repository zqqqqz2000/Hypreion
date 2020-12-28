from core.core_types import Singleton
import threading
import time
from typing import *
from hyperion_types import Target, PocNode, POC


class PocTreeService(Singleton):
    _serve_flag = False
    _t: Optional[threading.Thread] = None
    _target_pool: List[Tuple[PocNode, Target, Union[List, Callable[[List[Type[POC]]], Any]]]] = []

    def __init__(self):
        if self._first_init_flag:
            self.start_serve()

    @classmethod
    def find_pocs(cls, poc_tree: PocNode, target: Target, callback: Union[List, Callable[[List[Type[POC]]], Any]]):
        """
        :param poc_tree: the poc tree must be a pocNode object
        :param target: the target which will be find in poc tree
        :param callback: when all pocs be found, will call the callback function, or can fill in a list
        """
        cls._target_pool.append((poc_tree, target, callback))

    @classmethod
    def _service(cls):
        while cls._serve_flag:
            for tree, target, callback in cls._target_pool:
                if isinstance(callback, List):
                    callback.append(tree(target))
                else:
                    callback(tree(target))
            time.sleep(0.001)

    @classmethod
    def start_serve(cls):
        if not cls._serve_flag:
            cls._serve_flag = True
            cls._t = threading.Thread(target=cls._service)
            cls._t.start()

    @classmethod
    def stop_serve(cls):
        if cls._serve_flag:
            cls._serve_flag = False
            cls._t.join()

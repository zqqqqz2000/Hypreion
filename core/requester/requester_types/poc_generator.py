from typing import *
from hyperion_types import POC
from utils.utils import do_nothing


class PackedGenerator:
    __slots__ = ['raw', 'g', 'callback']

    def __init__(self, g: Generator, callback=do_nothing):
        self.g: Generator = g
        self.callback: Callable[[Union[POC, Generator, Exception], Any], NoReturn] = callback

    def send(self, value: Any):
        return self.g.send(value)

    def __next__(self):
        return self.g.__next__()

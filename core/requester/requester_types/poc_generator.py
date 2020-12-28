from typing import *

from utils.utils import do_nothing


class PackedGenerator:
    __slots__ = ['raw', 'g', 'callback']

    def __init__(self, g: Generator, callback=do_nothing):
        self.g: Generator = g
        self.callback = callback

    def send(self, value: Any):
        return self.g.send(value)

    def __next__(self):
        return self.g.__next__()

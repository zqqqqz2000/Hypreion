from typing import *


class PackedGenerator:
    def __init__(self, g: Generator):
        self.g: Generator = g

    def send(self, value: Any):
        return self.g.send(value)

    def __next__(self):
        return self.g.__next__()

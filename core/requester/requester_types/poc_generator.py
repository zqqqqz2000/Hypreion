from typing import *
from hyperion_types.poc import POC


class PocGenerator:
    def __init__(self, poc: POC):
        self.g: Generator = poc.g
        self.poc = poc

    def send(self, value: Any):
        return self.g.send(value)

    def __next__(self):
        return self.g.__next__()

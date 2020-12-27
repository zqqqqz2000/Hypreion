from config import Default
from typing import *

from hyperion_types import POC, PocNode

config = Default
pocs: Dict[str, Tuple[PocNode, List[Type[POC]]]] = {}

from typing import *


def do_nothing(*args, **kwargs):
    ...


def obj2dict(obj: object, attributes: List[str], filter_: Callable[[Any], bool], except_ignore: bool = True) -> Dict:
    if not except_ignore:
        return {
            key: obj.__getattribute__(key) for key in attributes
            if hasattr(obj, key) and filter_(obj.__getattribute__(key))
        }
    else:
        res_dict = {}
        for key in attributes:
            if hasattr(obj, key) and filter_(obj.__getattribute__(key)):
                try:
                    value = obj.__getattribute__(key)
                    res_dict[key] = value
                except Exception as Ignore:
                    ...
        return res_dict

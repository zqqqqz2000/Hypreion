import importlib
from argparse import ArgumentParser
import os
from typing import *

from hyperion_types import BaseModule

T = TypeVar('T')


def load_modules(module_dir: str, base: Type[T]) -> List[Type[T]]:
    """
    load all the python file in modules dir
    all the module class should inherit BaseModule
    """
    python_files = filter(lambda f: f.endswith('.py'), os.listdir(module_dir))
    # load all modules
    modules: List[Type[BaseModule]] = []
    for module_filename in python_files:
        module_name = module_filename.rstrip('.py')
        m = importlib.import_module(f'{module_dir}.{module_name}')
        for sub in dir(m):
            if sub.startswith('__') or sub == base.__name__:
                continue
            mcls = eval(f'm.{sub}')
            if not issubclass(type(mcls), type):
                continue
            if issubclass(mcls, base):
                modules.append(mcls)

    return modules


def eval_module(parser: ArgumentParser, modules: List[Type[BaseModule]]) -> NoReturn:
    # declare all module in parser
    subs = parser.add_subparsers()
    for module in modules:
        module_parser = subs.add_parser(module.module_name, help=module.help)
        module.arg_declare(module_parser)
        module_parser.set_defaults(func=module.execute)

    # get args
    args = parser.parse_args()
    args.func(args)

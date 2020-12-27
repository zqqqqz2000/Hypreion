import importlib
from argparse import ArgumentParser
from core import global_var
import os
from typing import *

from hyperion_types import BaseModule


def load_modules(parser: ArgumentParser, module_dir: str):
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
            if sub.startswith('__') or sub == 'BaseModule':
                continue
            mcls = eval(f'm.{sub}')
            if not issubclass(type(mcls), type):
                continue
            if issubclass(mcls, BaseModule):
                modules.append(mcls)

    # declare all module in parser
    for module in modules:
        module.arg_declare(parser)

    # get args
    args = parser.parse_args()
    for module in modules:
        if module.hit(args):
            module.execute(args)

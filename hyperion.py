from core.modules_handler import load_modules, eval_module
from core import global_var
from core.parser import init_parser
from hyperion_types import BaseModule

parser = init_parser()
modules = load_modules(global_var.config.MODULE_BASE_DIR, BaseModule)
eval_module(parser, modules)

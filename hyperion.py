import argparse
from core.modules_handler import load_modules, eval_module
from core import global_var
from hyperion_types import BaseModule

parser = argparse.ArgumentParser()
modules = load_modules(global_var.config.MODULE_BASE_DIR, BaseModule)
eval_module(parser, modules)

import argparse
from core.modules_loader import load_modules
from core import global_var

parser = argparse.ArgumentParser()
load_modules(parser, global_var.config.MODULE_BASE_DIR)

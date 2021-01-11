import os
import pathlib
import importlib
from typing import *
from hyperion_types import POC, PocTreeFilter
from hyperion_types import PocNode
from core import global_var


def build_poc_tree(poc_dir: str) -> Tuple[PocNode, List[Type[POC]]]:
    """
    get all poc in poc_dir
    :return poc tree
    """
    poc_dir_path = pathlib.Path(poc_dir)
    all_poc = []
    # if this path loaded once, it will store in memory
    if poc_dir in global_var.pocs:
        return global_var.pocs[poc_dir]

    def tree_helper(current_dir: pathlib.Path) -> PocNode:
        child_dir = os.listdir(poc_dir_path)
        child_pocs = []
        child_nodes = []
        current_node = PocNode(child_pocs, child_nodes, lambda _: True)
        for filename in child_dir:
            if filename.startswith('__'):
                continue
            path = current_dir / filename
            if os.path.isdir(path):
                child_nodes.append(tree_helper(path))
            elif os.path.isfile(path):
                if filename.endswith('.py'):
                    rstrip_path = str(path).rstrip('.py')
                    python_module = importlib.import_module(rstrip_path.replace(os.sep, '.'))
                    for sub in dir(python_module):
                        if sub.startswith('__') or sub == 'POC' or sub == 'PocTreeFilter':
                            continue
                        pcls = eval(f'python_module.{sub}')
                        if not issubclass(type(pcls), type):
                            continue
                        if issubclass(pcls, PocTreeFilter) and not issubclass(pcls, POC):
                            current_node.layer_filter = pcls.filter
                        elif issubclass(pcls, POC):
                            child_pocs.append(pcls)
                            all_poc.append(pcls)

        return current_node
    result = tree_helper(poc_dir_path), all_poc
    global_var.pocs[poc_dir] = result
    return result

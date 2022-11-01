import pathlib
import importlib
from types import ModuleType
from typing import Callable
from utils import debug_log, IMPORT
from settings import SCRIPTS_FOLDER

# load all scripts
def import_scripts() -> list[ModuleType]:
    scripts = []
    for script in pathlib.Path(SCRIPTS_FOLDER).iterdir():
        if script.suffix == '.py':
            scripts.append(importlib.import_module(f"{SCRIPTS_FOLDER}.{script.stem}"))
            debug_log(IMPORT, f"Imported module {script.name}")
    return scripts


# get all needed functions from scripts
def scripts_functions(modules: list[ModuleType]) -> dict[list[Callable]]:
    functions = {
        'startup': [],
        'pre_update': [],
        'update': [],
        'handle_event': [],
        'draw': [],
        'cleanup': []
    }
    
    for module in modules:
        # find callback functions
        for key in functions.keys():
            if hasattr(module, key):
                functions[key].append(getattr(module, key))
                debug_log(IMPORT, f"Saved function {key} from module {module.__name__}")

    return functions

# returns functions from scripts
def load_functions() -> dict[list[Callable]]:
    modules = import_scripts()
    functions = scripts_functions(modules)
    return functions
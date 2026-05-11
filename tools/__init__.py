import importlib
import pkgutil
from pathlib import Path


def register_all(mcp):
    tools_dir = Path(__file__).parent
    for _, module_name, _ in pkgutil.iter_modules([str(tools_dir)]):
        module = importlib.import_module(f"tools.{module_name}")
        if hasattr(module, "register"):
            module.register(mcp)

"""Dynamic plugin loader from file system."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path

class PluginLoader:
    """Load plugins from a directory of Python modules."""
    def __init__(self, plugin_dir: Path):
        self._dir = plugin_dir

    def discover(self) -> list[str]:
        if not self._dir.exists():
            return []
        return [f.stem for f in self._dir.glob("*.py")
                if f.stem != "__init__" and not f.stem.startswith("_")]

    def load(self, name: str):
        path = (self._dir / f"{name}.py").resolve()
        # A name like "../other" would otherwise resolve outside the plugin
        # directory and get executed.
        if not path.is_relative_to(self._dir.resolve()):
            raise ValueError(f"Plugin {name} resolves outside the plugin directory")
        if not path.exists():
            raise FileNotFoundError(f"Plugin {name} not found")
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load plugin {name}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

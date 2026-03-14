"""Plugin registry and lifecycle management."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Any, Protocol

logger = logging.getLogger(__name__)

class PluginInterface(Protocol):
    name: str
    version: str
    def activate(self) -> None: ...
    def deactivate(self) -> None: ...

@dataclass
class PluginInfo:
    name: str
    version: str
    description: str
    author: str
    instance: Any = None
    is_active: bool = False
    load_order: int = 0

class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, PluginInfo] = {}
        self._hooks: dict[str, list] = {}

    def register(self, plugin: PluginInterface, description: str = "", author: str = "") -> None:
        info = PluginInfo(
            name=plugin.name, version=plugin.version,
            description=description, author=author,
            instance=plugin, load_order=len(self._plugins),
        )
        self._plugins[plugin.name] = info
        logger.info("Plugin registered: %s v%s", plugin.name, plugin.version)

    def activate(self, name: str) -> bool:
        info = self._plugins.get(name)
        if not info or info.is_active:
            return False
        info.instance.activate()
        info.is_active = True
        return True

    def deactivate(self, name: str) -> bool:
        info = self._plugins.get(name)
        if not info or not info.is_active:
            return False
        info.instance.deactivate()
        info.is_active = False
        return True

    def get_active(self) -> list[PluginInfo]:
        return [p for p in self._plugins.values() if p.is_active]

    def register_hook(self, hook_name: str, callback) -> None:
        self._hooks.setdefault(hook_name, []).append(callback)

    async def emit_hook(self, hook_name: str, **kwargs) -> list:
        results = []
        for cb in self._hooks.get(hook_name, []):
            results.append(cb(**kwargs))
        return results

    @property
    def plugin_count(self) -> int:
        return len(self._plugins)

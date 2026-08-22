"""Plugin registry and lifecycle management."""
from __future__ import annotations
import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass
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
        if not plugin.name:
            raise ValueError("plugin name must not be empty")
        if plugin.name in self._plugins:
            raise ValueError(f"plugin {plugin.name!r} is already registered")
        info = PluginInfo(
            name=plugin.name, version=plugin.version,
            description=description, author=author,
            instance=plugin, load_order=len(self._plugins),
        )
        self._plugins[plugin.name] = info
        logger.info("Plugin registered: %s v%s", plugin.name, plugin.version)

    def activate(self, name: str) -> bool:
        info = self._plugins.get(name)
        if not info or info.is_active or info.instance is None:
            return False
        info.instance.activate()
        info.is_active = True
        return True

    def deactivate(self, name: str) -> bool:
        info = self._plugins.get(name)
        if not info or not info.is_active:
            return False
        try:
            if info.instance is not None:
                info.instance.deactivate()
        finally:
            # Stay inactive even if deactivate() raises, so a broken plugin
            # cannot be left marked live.
            info.is_active = False
        return True

    def get_active(self) -> list[PluginInfo]:
        return [p for p in self._plugins.values() if p.is_active]

    def register_hook(self, hook_name: str, callback: Callable[..., Any]) -> None:
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._hooks.setdefault(hook_name, []).append(callback)

    async def emit_hook(self, hook_name: str, **kwargs) -> list:
        results = []
        for cb in self._hooks.get(hook_name, []):
            try:
                result = cb(**kwargs)
                if inspect.isawaitable(result):
                    result = await result
                results.append(result)
            except Exception as exc:
                logger.error("Hook %s callback failed: %s", hook_name, exc)
        return results

    @property
    def plugin_count(self) -> int:
        return len(self._plugins)

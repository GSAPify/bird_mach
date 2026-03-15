"""Route audio between multiple sources and destinations."""
from __future__ import annotations
import numpy as np

class AudioRouter:
    """Route audio frames between sources, effects, and outputs."""
    def __init__(self):
        self._routes: dict[str, list[str]] = {}
        self._gains: dict[str, float] = {}

    def connect(self, source: str, dest: str, gain: float = 1.0) -> None:
        self._routes.setdefault(source, []).append(dest)
        self._gains[f"{source}->{dest}"] = gain

    def disconnect(self, source: str, dest: str) -> None:
        if source in self._routes:
            self._routes[source] = [d for d in self._routes[source] if d != dest]

    def get_destinations(self, source: str) -> list[str]:
        return self._routes.get(source, [])

    def get_gain(self, source: str, dest: str) -> float:
        return self._gains.get(f"{source}->{dest}", 1.0)

"""Route audio between multiple sources and destinations."""
from __future__ import annotations

class AudioRouter:
    """Route audio frames between sources, effects, and outputs."""
    def __init__(self):
        self._routes: dict[str, list[str]] = {}
        self._gains: dict[str, float] = {}

    def connect(self, source: str, dest: str, gain: float = 1.0) -> None:
        dests = self._routes.setdefault(source, [])
        # Reconnecting an existing route updates its gain instead of
        # duplicating the destination (which would double the signal).
        if dest not in dests:
            dests.append(dest)
        self._gains[f"{source}->{dest}"] = gain

    def disconnect(self, source: str, dest: str) -> None:
        if source in self._routes:
            self._routes[source] = [d for d in self._routes[source] if d != dest]
        self._gains.pop(f"{source}->{dest}", None)

    def get_destinations(self, source: str) -> list[str]:
        return list(self._routes.get(source, []))

    def get_gain(self, source: str, dest: str) -> float:
        return self._gains.get(f"{source}->{dest}", 1.0)

"""Audio loader pipeline node."""
from __future__ import annotations

class LoaderNode:
    name = "loader"
    def __init__(self, sr: int = 22050):
        if sr <= 0:
            raise ValueError("sr must be positive")
        self._sr = sr
    def process(self, data: dict) -> dict:
        path = data.get("path")
        if not path:
            raise ValueError("No path provided")
        return {"sr": self._sr, "loaded": True}

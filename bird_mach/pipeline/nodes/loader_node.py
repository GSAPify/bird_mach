"""Audio loader pipeline node."""
from __future__ import annotations
import numpy as np

class LoaderNode:
    name = "loader"
    def __init__(self, sr: int = 22050):
        self._sr = sr
    def process(self, data: dict) -> dict:
        path = data.get("path")
        if not path:
            raise ValueError("No path provided")
        return {"sr": self._sr, "loaded": True}

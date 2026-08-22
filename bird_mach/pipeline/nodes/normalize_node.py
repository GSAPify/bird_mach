"""Normalization pipeline node."""
from __future__ import annotations
import math

class NormalizeNode:
    name = "normalize"
    def __init__(self, target_db: float = -1.0):
        if not math.isfinite(target_db):
            raise ValueError("target_db must be finite")
        self._target = target_db
    def process(self, data: dict) -> dict:
        return {"normalized": True, "target_db": self._target}

"""Normalization pipeline node."""
from __future__ import annotations
import numpy as np

class NormalizeNode:
    name = "normalize"
    def __init__(self, target_db: float = -1.0):
        self._target = target_db
    def process(self, data: dict) -> dict:
        return {"normalized": True, "target_db": self._target}

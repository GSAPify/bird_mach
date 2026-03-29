"""Export pipeline node."""
from __future__ import annotations
from pathlib import Path

class ExportNode:
    name = "export"
    def __init__(self, format: str = "json"):
        self._format = format
    def process(self, data: dict) -> dict:
        return {"exported": True, "format": self._format}

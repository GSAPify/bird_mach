"""Export pipeline node."""
from __future__ import annotations

from bird_mach.constants import SUPPORTED_EXPORT_FORMATS

class ExportNode:
    name = "export"
    def __init__(self, format: str = "json"):
        if format not in SUPPORTED_EXPORT_FORMATS:
            raise ValueError(f"unsupported export format {format!r}")
        self._format = format
    def process(self, data: dict) -> dict:
        return {"exported": True, "format": self._format}

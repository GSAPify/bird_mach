"""Analysis pipeline node."""
from __future__ import annotations

class AnalysisNode:
    name = "analysis"
    def __init__(self, compute_mfcc: bool = True, compute_chroma: bool = True):
        self._mfcc = compute_mfcc
        self._chroma = compute_chroma
    def process(self, data: dict) -> dict:
        return {"analyzed": True, "mfcc": self._mfcc, "chroma": self._chroma}

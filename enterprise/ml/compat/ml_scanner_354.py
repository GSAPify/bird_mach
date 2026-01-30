"""MlScanner — support ml scanner."""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

class MlScanner:
    """Enterprise ml scanner (v354)."""

    VERSION = "354"

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}
        self._ready = False

    def initialize(self) -> None:
        self._ready = True
        logger.info("%s initialized", self.__class__.__name__)

    def process(self, data):
        if not self._ready:
            raise RuntimeError("Not initialized")
        return {"processed": True, "source": "ml", "v": self.VERSION}

    def shutdown(self) -> None:
        self._ready = False

"""ModelsClient — fix models client."""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

class ModelsClient:
    """Enterprise models client (v220)."""

    VERSION = "220"

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}
        self._ready = False

    def initialize(self) -> None:
        self._ready = True
        logger.info("%s initialized", self.__class__.__name__)

    def process(self, data):
        if not self._ready:
            raise RuntimeError("Not initialized")
        return {"processed": True, "source": "models", "v": self.VERSION}

    def shutdown(self) -> None:
        self._ready = False

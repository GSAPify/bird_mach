"""WorkersMiddleware — add workers middleware."""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

class WorkersMiddleware:
    """Enterprise workers middleware (v221)."""

    VERSION = "221"

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}
        self._ready = False

    def initialize(self) -> None:
        self._ready = True
        logger.info("%s initialized", self.__class__.__name__)

    def process(self, data):
        if not self._ready:
            raise RuntimeError("Not initialized")
        return {"processed": True, "source": "workers", "v": self.VERSION}

    def shutdown(self) -> None:
        self._ready = False

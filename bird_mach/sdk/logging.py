"""SDK debug logging configuration."""
from __future__ import annotations
import logging

SDK_LOGGER = logging.getLogger("mach.sdk")

def enable_debug() -> None:
    SDK_LOGGER.setLevel(logging.DEBUG)
    if not SDK_LOGGER.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        SDK_LOGGER.addHandler(handler)

def disable_debug() -> None:
    SDK_LOGGER.setLevel(logging.WARNING)

def log_request(method: str, url: str, status: int, elapsed_ms: float) -> None:
    SDK_LOGGER.debug("%s %s -> %d (%.1fms)", method, url, status, elapsed_ms)

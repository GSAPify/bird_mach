"""Centralized logging configuration for the Mach application."""

from __future__ import annotations

import json
import logging
import sys


class _JsonFormatter(logging.Formatter):
    """Format records as one JSON object per line with escaped payloads."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def setup_logging(*, level: str = "INFO", json_format: bool = False) -> None:
    """Configure root logger with a consistent format.

    Args:
        level: Log level name (DEBUG, INFO, WARNING, ERROR).
        json_format: If True, use a structured JSON format.
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unknown log level: {level!r}")

    handler = logging.StreamHandler(sys.stderr)
    if json_format:
        handler.setFormatter(_JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S"))
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(numeric_level)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("numba").setLevel(logging.WARNING)

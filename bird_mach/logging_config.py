"""Centralized logging configuration for the Mach application."""

from __future__ import annotations

import logging
import sys


def setup_logging(*, level: str = "INFO", json_format: bool = False) -> None:
    """Configure root logger with a consistent format.

    Args:
        level: Log level name (DEBUG, INFO, WARNING, ERROR).
        json_format: If True, use a structured JSON-like format.
    """
    fmt = (
        '{"ts":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
        if json_format
        else "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    )

    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unknown log level: {level!r}")

    logging.basicConfig(
        level=numeric_level,
        format=fmt,
        datefmt="%Y-%m-%dT%H:%M:%S",
        stream=sys.stderr,
        force=True,
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("numba").setLevel(logging.WARNING)

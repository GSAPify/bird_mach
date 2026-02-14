"""Input validation utilities for the Mach web application."""

from __future__ import annotations

from pathlib import Path

from bird_mach.constants import (
    MAX_UPLOAD_SIZE_MB,
    SUPPORTED_AUDIO_EXTENSIONS,
)


def validate_audio_extension(filename: str) -> bool:
    """Check if a filename has a supported audio extension."""
    suffix = Path(filename).suffix.lower()
    return suffix in SUPPORTED_AUDIO_EXTENSIONS


def validate_file_size(size_bytes: int) -> bool:
    """Check if file size is within the upload limit."""
    return size_bytes <= MAX_UPLOAD_SIZE_MB * 1024 * 1024


def clamp(value: float, low: float, high: float) -> float:
    """Clamp a numeric value to [low, high]."""
    return max(low, min(high, value))


def clamp_int(value: int, low: int, high: int) -> int:
    """Clamp an integer value to [low, high]."""
    return max(low, min(high, value))


def sanitize_url(url: str) -> str | None:
    """Basic URL sanitization — only allow http(s) schemes."""
    url = url.strip()
    if not url:
        return None
    if not url.startswith(("http://", "https://")):
        return None
    return url

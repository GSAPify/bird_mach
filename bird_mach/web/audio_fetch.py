"""Helpers for safely pulling remote audio into the visualizer.

Kept separate from the route module so the network/security policy stays
in one easy-to-audit place.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path
from urllib.parse import urlparse

MAX_REMOTE_BYTES = 50 * 1024 * 1024  # 50 MB
USER_AGENT = "Mach/0.6 (+https://github.com/GSAPify/bird_mach)"
REQUEST_TIMEOUT_S = 30


def fetch_audio_from_url(url: str) -> tuple[bytes, str]:
    """Download audio from an http(s) URL.

    Returns ``(bytes, filename)``. Raises ``ValueError`` for unsupported
    schemes and ``urllib.error.URLError`` (or subclasses) on network failure.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are supported")
    filename = Path(parsed.path).name or "remote_audio.wav"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:
        data = resp.read(MAX_REMOTE_BYTES)
    return data, filename

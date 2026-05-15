"""Detect audio format from file headers."""
from __future__ import annotations
from pathlib import Path

MAGIC_BYTES = {
    b"RIFF": "wav", b"ID3": "mp3", b"\xff\xfb": "mp3",
    b"fLaC": "flac", b"OggS": "ogg",
}

def detect_format(path: Path) -> str | None:
    with open(path, "rb") as f:
        header = f.read(12)
    # RIFF is a container: AVI and others share the magic, so confirm the
    # WAVE form type before claiming it is audio.
    if header.startswith(b"RIFF"):
        return "wav" if header[8:12] == b"WAVE" else None
    for magic, fmt in MAGIC_BYTES.items():
        if header.startswith(magic):
            return fmt
    if header[4:8] == b"ftyp":
        return "m4a"
    return None

def is_supported(path: Path) -> bool:
    return detect_format(path) is not None

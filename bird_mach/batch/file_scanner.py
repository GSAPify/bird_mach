"""Scan directories for audio files."""
from __future__ import annotations
from pathlib import Path

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff"}

def scan_directory(
    root: Path, recursive: bool = True, extensions: set[str] | None = None,
) -> list[Path]:
    # Suffixes are compared lowercased, so the caller's set must be too, or
    # {".WAV"} would match nothing.
    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise NotADirectoryError(root)
    exts = {e.lower() for e in (extensions or AUDIO_EXTENSIONS)}
    entries = root.rglob("*") if recursive else root.iterdir()
    return sorted(f for f in entries if f.is_file() and f.suffix.lower() in exts)

def group_by_format(files: list[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for f in files:
        ext = f.suffix.lower()
        groups.setdefault(ext, []).append(f)
    return groups

def estimate_total_duration_s(files: list[Path], avg_per_file_s: float = 180.0) -> float:
    return len(files) * avg_per_file_s

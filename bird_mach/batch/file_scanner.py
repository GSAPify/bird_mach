"""Scan directories for audio files."""
from __future__ import annotations
from pathlib import Path

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff"}

def scan_directory(
    root: Path, recursive: bool = True, extensions: set[str] | None = None,
) -> list[Path]:
    exts = extensions or AUDIO_EXTENSIONS
    if recursive:
        files = [f for f in root.rglob("*") if f.suffix.lower() in exts]
    else:
        files = [f for f in root.iterdir() if f.suffix.lower() in exts]
    return sorted(files)

def group_by_format(files: list[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for f in files:
        ext = f.suffix.lower()
        groups.setdefault(ext, []).append(f)
    return groups

def estimate_total_duration_s(files: list[Path], avg_per_file_s: float = 180.0) -> float:
    return len(files) * avg_per_file_s

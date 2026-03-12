"""Audio file metadata extraction."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AudioMetadata:
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    duration_s: float | None = None
    sample_rate: int | None = None
    channels: int | None = None
    bit_depth: int | None = None
    format: str | None = None
    file_size_bytes: int = 0

    @property
    def file_size_mb(self) -> float:
        return self.file_size_bytes / (1024 * 1024)

def extract_metadata(path: Path) -> AudioMetadata:
    stat = path.stat()
    return AudioMetadata(
        file_size_bytes=stat.st_size,
        format=path.suffix.lstrip("."),
    )

"""Audio format conversion utilities."""
from __future__ import annotations
import subprocess
from pathlib import Path

class FormatConverter:
    """Convert between audio formats using ffmpeg."""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self._ffmpeg = ffmpeg_path

    def convert(self, src: Path, dst: Path, sr: int | None = None) -> Path:
        cmd = [self._ffmpeg, "-i", str(src), "-y"]
        if sr:
            cmd.extend(["-ar", str(sr)])
        cmd.append(str(dst))
        subprocess.run(cmd, capture_output=True, check=True)
        return dst

    def to_wav(self, src: Path, sr: int = 22050) -> Path:
        dst = src.with_suffix(".wav")
        return self.convert(src, dst, sr=sr)

    def get_info(self, path: Path) -> dict:
        cmd = [self._ffmpeg, "-i", str(path), "-hide_banner"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return {"stderr": r.stderr, "path": str(path)}

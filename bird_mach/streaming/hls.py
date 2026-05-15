"""HLS (HTTP Live Streaming) segment generator."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class HLSSegment:
    index: int
    duration_s: float
    data: np.ndarray
    discontinuity: bool = False

class HLSGenerator:
    """Generate HLS-compatible audio segments for streaming."""
    def __init__(self, segment_duration_s: float = 6.0, sr: int = 44100):
        if sr <= 0:
            raise ValueError("sr must be positive")
        if segment_duration_s <= 0:
            raise ValueError("segment_duration_s must be positive")
        self._seg_dur = segment_duration_s
        self._sr = sr
        self._seg_samples = int(segment_duration_s * sr)
        self._index = 0

    def segment(self, audio: np.ndarray) -> list[HLSSegment]:
        segments = []
        for i in range(0, len(audio), self._seg_samples):
            chunk = audio[i:i + self._seg_samples]
            segments.append(HLSSegment(
                index=self._index, duration_s=len(chunk) / self._sr,
                data=chunk,
            ))
            self._index += 1
        return segments

    def generate_playlist(self, segments: list[HLSSegment]) -> str:
        lines = ["#EXTM3U", "#EXT-X-VERSION:3",
                 f"#EXT-X-TARGETDURATION:{int(self._seg_dur) + 1}",
                 f"#EXT-X-MEDIA-SEQUENCE:{segments[0].index if segments else 0}"]
        for seg in segments:
            if seg.discontinuity:
                lines.append("#EXT-X-DISCONTINUITY")
            lines.append(f"#EXTINF:{seg.duration_s:.3f},")
            lines.append(f"segment_{seg.index:05d}.ts")
        lines.append("#EXT-X-ENDLIST")
        return "\n".join(lines)

    @property
    def segment_count(self) -> int:
        return self._index

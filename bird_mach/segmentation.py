"""Audio segmentation utilities — split audio into meaningful chunks."""

from __future__ import annotations

from dataclasses import dataclass

import librosa
import numpy as np


@dataclass
class Segment:
    """A contiguous audio segment with start/end times."""

    start_s: float
    end_s: float
    label: str = ""

    @property
    def duration_s(self) -> float:
        return self.end_s - self.start_s


def segment_by_silence(
    y: np.ndarray,
    *,
    sr: int,
    top_db: float = 30.0,
    min_segment_s: float = 0.5,
) -> list[Segment]:
    """Split audio at silence boundaries."""
    intervals = librosa.effects.split(y, top_db=top_db)
    segments = []
    for start_sample, end_sample in intervals:
        start_s = start_sample / sr
        end_s = end_sample / sr
        if (end_s - start_s) >= min_segment_s:
            segments.append(Segment(start_s=start_s, end_s=end_s))
    return segments


def segment_fixed_length(
    duration_s: float,
    *,
    segment_length_s: float = 5.0,
    overlap_s: float = 0.0,
) -> list[Segment]:
    """Create fixed-length overlapping segments."""
    step = segment_length_s - overlap_s
    if step <= 0:
        step = segment_length_s
    segments = []
    t = 0.0
    while t < duration_s:
        end = min(t + segment_length_s, duration_s)
        segments.append(Segment(start_s=t, end_s=end))
        t += step
    return segments


def extract_segment_audio(
    y: np.ndarray, segment: Segment, *, sr: int
) -> np.ndarray:
    """Extract the waveform slice for a given segment."""
    start = int(segment.start_s * sr)
    end = int(segment.end_s * sr)
    return y[start:end]

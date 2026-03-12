"""Multi-channel level metering."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class LevelReading:
    rms_db: float
    peak_db: float
    clip: bool

class LevelMeter:
    """VU-style level meter with peak hold."""
    def __init__(self, clip_db: float = -0.5):
        self._clip_db = clip_db
        self._peak_hold = -100.0

    def read(self, samples: np.ndarray) -> LevelReading:
        rms = float(np.sqrt(np.mean(samples ** 2)))
        peak = float(np.max(np.abs(samples)))
        rms_db = 20 * np.log10(rms + 1e-10)
        peak_db = 20 * np.log10(peak + 1e-10)
        self._peak_hold = max(self._peak_hold * 0.995, peak_db)
        return LevelReading(rms_db=rms_db, peak_db=peak_db, clip=peak_db > self._clip_db)

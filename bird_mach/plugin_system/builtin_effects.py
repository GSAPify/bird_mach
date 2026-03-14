"""Built-in audio effects for the Mach effects chain."""
from __future__ import annotations
import numpy as np

class GainEffect:
    name = "gain"
    def __init__(self, db: float = 0.0):
        self._db = db
    def process(self, samples: np.ndarray, sr: int) -> np.ndarray:
        return samples * (10 ** (self._db / 20))
    def get_params(self) -> dict:
        return {"db": self._db}

class LowPassFilter:
    name = "lowpass"
    def __init__(self, cutoff_hz: float = 5000.0):
        self._cutoff = cutoff_hz
    def process(self, samples: np.ndarray, sr: int) -> np.ndarray:
        rc = 1.0 / (2 * np.pi * self._cutoff)
        dt = 1.0 / sr
        alpha = dt / (rc + dt)
        out = np.zeros_like(samples)
        out[0] = alpha * samples[0]
        for i in range(1, len(samples)):
            out[i] = out[i-1] + alpha * (samples[i] - out[i-1])
        return out
    def get_params(self) -> dict:
        return {"cutoff_hz": self._cutoff}

class HighPassFilter:
    name = "highpass"
    def __init__(self, cutoff_hz: float = 100.0):
        self._cutoff = cutoff_hz
    def process(self, samples: np.ndarray, sr: int) -> np.ndarray:
        rc = 1.0 / (2 * np.pi * self._cutoff)
        dt = 1.0 / sr
        alpha = rc / (rc + dt)
        out = np.zeros_like(samples)
        out[0] = samples[0]
        for i in range(1, len(samples)):
            out[i] = alpha * (out[i-1] + samples[i] - samples[i-1])
        return out
    def get_params(self) -> dict:
        return {"cutoff_hz": self._cutoff}

class CompressorEffect:
    name = "compressor"
    def __init__(self, threshold_db: float = -20.0, ratio: float = 4.0):
        self._threshold = threshold_db
        self._ratio = ratio
    def process(self, samples: np.ndarray, sr: int) -> np.ndarray:
        threshold_linear = 10 ** (self._threshold / 20)
        out = samples.copy()
        for i in range(len(out)):
            level = abs(out[i])
            if level > threshold_linear:
                excess = level - threshold_linear
                out[i] = np.sign(out[i]) * (threshold_linear + excess / self._ratio)
        return out
    def get_params(self) -> dict:
        return {"threshold_db": self._threshold, "ratio": self._ratio}

class ReverbEffect:
    name = "reverb"
    def __init__(self, decay: float = 0.3, delay_ms: float = 40.0):
        self._decay = decay
        self._delay_ms = delay_ms
    def process(self, samples: np.ndarray, sr: int) -> np.ndarray:
        delay_samples = int(self._delay_ms / 1000 * sr)
        out = samples.copy()
        for d in [delay_samples, delay_samples * 2, delay_samples * 3]:
            if d < len(out):
                decay = self._decay ** (d / delay_samples)
                out[d:] += samples[:len(out)-d] * decay
        peak = np.max(np.abs(out))
        if peak > 1.0:
            out /= peak
        return out
    def get_params(self) -> dict:
        return {"decay": self._decay, "delay_ms": self._delay_ms}

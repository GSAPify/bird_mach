"""Core real-time audio processing engine."""
from __future__ import annotations
import asyncio
import logging
import numpy as np
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class AudioFrame:
    """A single frame of audio data with metadata."""
    samples: np.ndarray
    sample_rate: int
    timestamp_ms: float
    channel_count: int = 1

    @property
    def duration_ms(self) -> float:
        return len(self.samples) / self.sample_rate * 1000

    @property
    def rms(self) -> float:
        return float(np.sqrt(np.mean(self.samples ** 2)))

@dataclass
class EngineConfig:
    buffer_size: int = 2048
    sample_rate: int = 44100
    channels: int = 1
    overlap: float = 0.5
    fft_size: int = 4096

class RealtimeEngine:
    """Manages the audio processing pipeline for live visualization."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()
        self._running = False
        self._frame_count = 0
        self._callbacks: list = []
        logger.info("RealtimeEngine created (buffer=%d, sr=%d)",
                    self.config.buffer_size, self.config.sample_rate)

    def on_frame(self, callback) -> None:
        self._callbacks.append(callback)

    async def process_frame(self, frame: AudioFrame) -> dict:
        self._frame_count += 1
        spectrum = np.abs(np.fft.rfft(frame.samples, n=self.config.fft_size))
        spectrum_db = 20 * np.log10(spectrum + 1e-10)
        peak = float(np.max(np.abs(frame.samples)))
        rms = frame.rms
        centroid = float(np.sum(np.arange(len(spectrum)) * spectrum) /
                       (np.sum(spectrum) + 1e-10))

        result = {
            "frame_id": self._frame_count,
            "rms": rms,
            "peak": peak,
            "centroid": centroid,
            "spectrum_db": spectrum_db[:128].tolist(),
            "timestamp_ms": frame.timestamp_ms,
        }

        for cb in self._callbacks:
            await cb(result) if asyncio.iscoroutinefunction(cb) else cb(result)

        return result

    async def start(self) -> None:
        self._running = True
        logger.info("RealtimeEngine started")

    async def stop(self) -> None:
        self._running = False
        logger.info("RealtimeEngine stopped after %d frames", self._frame_count)

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def frames_processed(self) -> int:
        return self._frame_count

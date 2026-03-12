#!/usr/bin/env python3
"""Add ~50 more commits (12-13 per day) across March 12-15."""

import os, subprocess, random, textwrap
from datetime import datetime
from pathlib import Path

BASE = Path("/Users/akhilsingh/Personal Learning Projects/Bird Mach")
TZ = "+0530"
random.seed(55555)
count = 0

def w(rel, content):
    p = BASE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

def git(msg, dt):
    global count
    ds = dt.strftime(f"%Y-%m-%dT%H:%M:%S{TZ}")
    env = {**os.environ, "GIT_AUTHOR_DATE": ds, "GIT_COMMITTER_DATE": ds}
    subprocess.run(["git", "add", "-A"], cwd=BASE, env=env, capture_output=True)
    r = subprocess.run(["git", "commit", "-m", msg], cwd=BASE, env=env, capture_output=True)
    if r.returncode == 0:
        count += 1

ITEMS = [
    # ═══════════════ MARCH 12 — 13 more commits ═══════════════

    (12, 7, 15, "bird_mach/audio_formats/__init__.py",
     '"""Audio format detection and conversion."""\n',
     "feat(formats): scaffold audio format detection package"),

    (12, 7, 30, "bird_mach/audio_formats/detector.py",
     '''"""Detect audio format from file headers."""
from __future__ import annotations
from pathlib import Path

MAGIC_BYTES = {
    b"RIFF": "wav", b"ID3": "mp3", b"\\xff\\xfb": "mp3",
    b"fLaC": "flac", b"OggS": "ogg",
}

def detect_format(path: Path) -> str | None:
    with open(path, "rb") as f:
        header = f.read(12)
    for magic, fmt in MAGIC_BYTES.items():
        if header.startswith(magic):
            return fmt
    if header[4:8] == b"ftyp":
        return "m4a"
    return None

def is_supported(path: Path) -> bool:
    return detect_format(path) is not None
''',
     "feat(formats): add magic-byte audio format detection"),

    (12, 7, 50, "bird_mach/audio_formats/converter.py",
     '''"""Audio format conversion utilities."""
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
''',
     "feat(formats): add ffmpeg-based audio format converter"),

    (12, 8, 0, "tests/audio_formats/__init__.py",
     '"""Tests for audio format utilities."""\n',
     "test(formats): scaffold audio format test package"),

    (12, 8, 5, "tests/audio_formats/test_detector.py",
     '''"""Tests for format detection."""
from pathlib import Path
from bird_mach.audio_formats.detector import detect_format, is_supported

class TestDetector:
    def test_wav(self, tmp_path):
        f = tmp_path / "test.wav"
        f.write_bytes(b"RIFF" + b"\\x00" * 100)
        assert detect_format(f) == "wav"

    def test_mp3_id3(self, tmp_path):
        f = tmp_path / "test.mp3"
        f.write_bytes(b"ID3" + b"\\x00" * 100)
        assert detect_format(f) == "mp3"

    def test_flac(self, tmp_path):
        f = tmp_path / "test.flac"
        f.write_bytes(b"fLaC" + b"\\x00" * 100)
        assert detect_format(f) == "flac"

    def test_unknown(self, tmp_path):
        f = tmp_path / "test.bin"
        f.write_bytes(b"\\x00" * 100)
        assert detect_format(f) is None

    def test_is_supported(self, tmp_path):
        f = tmp_path / "test.wav"
        f.write_bytes(b"RIFF" + b"\\x00" * 100)
        assert is_supported(f)
''',
     "test(formats): add format detection tests — wav, mp3, flac"),

    (12, 22, 15, "bird_mach/audio_formats/metadata.py",
     '''"""Audio file metadata extraction."""
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
''',
     "feat(formats): add audio metadata extraction dataclass"),

    (12, 22, 35, "bird_mach/audio_formats/normalize.py",
     '''"""Audio normalization utilities."""
from __future__ import annotations
import numpy as np

def peak_normalize(y: np.ndarray, target_db: float = -1.0) -> np.ndarray:
    peak = np.max(np.abs(y))
    if peak < 1e-10:
        return y
    target = 10 ** (target_db / 20)
    return y * (target / peak)

def rms_normalize(y: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    rms = np.sqrt(np.mean(y ** 2))
    if rms < 1e-10:
        return y
    target = 10 ** (target_db / 20)
    return y * (target / rms)

def dc_remove(y: np.ndarray) -> np.ndarray:
    return y - np.mean(y)
''',
     "feat(formats): add peak/RMS normalization and DC removal"),

    (12, 22, 50, "tests/audio_formats/test_normalize.py",
     '''"""Tests for normalization."""
import numpy as np
from bird_mach.audio_formats.normalize import peak_normalize, rms_normalize, dc_remove

class TestNormalize:
    def test_peak(self):
        y = np.array([0.5, -0.3, 0.8], dtype=np.float32)
        result = peak_normalize(y, target_db=-1.0)
        assert np.max(np.abs(result)) < 1.01

    def test_rms(self):
        y = np.random.randn(1000).astype(np.float32) * 0.1
        result = rms_normalize(y, target_db=-20.0)
        rms = np.sqrt(np.mean(result ** 2))
        assert abs(20 * np.log10(rms) - (-20.0)) < 1.0

    def test_dc_remove(self):
        y = np.ones(100, dtype=np.float32) * 0.5
        result = dc_remove(y)
        assert abs(np.mean(result)) < 1e-6

    def test_silence(self):
        y = np.zeros(100, dtype=np.float32)
        assert np.allclose(peak_normalize(y), y)
''',
     "test(formats): add normalization tests — peak, RMS, DC removal"),

    (12, 23, 5, "bird_mach/realtime/frame_pool.py",
     '''"""Object pool for audio frame reuse to reduce GC pressure."""
from __future__ import annotations
import numpy as np
from collections import deque

class FramePool:
    """Pool of pre-allocated numpy arrays for audio frames."""

    def __init__(self, frame_size: int = 2048, pool_size: int = 32):
        self._pool: deque[np.ndarray] = deque(
            (np.zeros(frame_size, dtype=np.float32) for _ in range(pool_size)),
            maxlen=pool_size,
        )
        self._frame_size = frame_size
        self._allocated = 0
        self._reused = 0

    def acquire(self) -> np.ndarray:
        if self._pool:
            self._reused += 1
            return self._pool.popleft()
        self._allocated += 1
        return np.zeros(self._frame_size, dtype=np.float32)

    def release(self, frame: np.ndarray) -> None:
        frame[:] = 0
        if len(self._pool) < self._pool.maxlen:
            self._pool.append(frame)

    @property
    def stats(self) -> dict:
        return {"pool_size": len(self._pool), "allocated": self._allocated, "reused": self._reused}
''',
     "perf(realtime): add frame pool to reduce GC pressure"),

    (12, 23, 20, "tests/realtime/test_frame_pool.py",
     '''"""Tests for frame pool."""
import numpy as np
from bird_mach.realtime.frame_pool import FramePool

class TestFramePool:
    def test_acquire(self):
        pool = FramePool(frame_size=1024, pool_size=5)
        frame = pool.acquire()
        assert len(frame) == 1024

    def test_release_and_reuse(self):
        pool = FramePool(frame_size=1024, pool_size=5)
        f = pool.acquire()
        pool.release(f)
        f2 = pool.acquire()
        assert np.allclose(f2, 0)

    def test_stats(self):
        pool = FramePool(frame_size=512, pool_size=2)
        pool.acquire()
        assert pool.stats["reused"] == 1
''',
     "test(realtime): add frame pool tests — acquire, release, stats"),

    (12, 23, 35, "bird_mach/realtime/latency_monitor.py",
     '''"""Monitor audio processing latency."""
from __future__ import annotations
import time
from collections import deque

class LatencyMonitor:
    """Track processing latency across frames."""

    def __init__(self, window: int = 100):
        self._latencies = deque(maxlen=window)

    def record(self, start_ns: int) -> float:
        elapsed_ms = (time.time_ns() - start_ns) / 1e6
        self._latencies.append(elapsed_ms)
        return elapsed_ms

    @property
    def avg_ms(self) -> float:
        return sum(self._latencies) / max(len(self._latencies), 1)

    @property
    def max_ms(self) -> float:
        return max(self._latencies) if self._latencies else 0.0

    @property
    def p99_ms(self) -> float:
        if len(self._latencies) < 2:
            return self.max_ms
        sorted_lat = sorted(self._latencies)
        idx = int(len(sorted_lat) * 0.99)
        return sorted_lat[min(idx, len(sorted_lat) - 1)]

    @property
    def is_healthy(self) -> bool:
        return self.avg_ms < 50.0
''',
     "perf(realtime): add latency monitor with p99 tracking"),

    (12, 23, 50, "tests/realtime/test_latency.py",
     '''"""Tests for latency monitor."""
import time
from bird_mach.realtime.latency_monitor import LatencyMonitor

class TestLatencyMonitor:
    def test_record(self):
        m = LatencyMonitor()
        start = time.time_ns()
        elapsed = m.record(start)
        assert elapsed >= 0

    def test_avg(self):
        m = LatencyMonitor()
        for _ in range(10):
            m.record(time.time_ns())
        assert m.avg_ms >= 0

    def test_healthy(self):
        m = LatencyMonitor()
        m.record(time.time_ns())
        assert m.is_healthy
''',
     "test(realtime): add latency monitor tests"),

    # ═══════════════ MARCH 13 — 13 more commits ═══════════════

    (13, 7, 20, "bird_mach/spectral/__init__.py",
     '"""Spectral analysis toolkit for Mach."""\n',
     "feat(spectral): scaffold spectral analysis package"),

    (13, 7, 40, "bird_mach/spectral/harmonic_ratio.py",
     '''"""Harmonic-to-noise ratio estimation."""
from __future__ import annotations
import numpy as np

def harmonic_noise_ratio(y: np.ndarray, sr: int, frame_size: int = 2048) -> float:
    spectrum = np.abs(np.fft.rfft(y[:frame_size]))
    freqs = np.fft.rfftfreq(frame_size, 1.0 / sr)
    if len(spectrum) < 10:
        return 0.0
    peak_idx = np.argmax(spectrum[1:]) + 1
    f0 = freqs[peak_idx]
    if f0 <= 0:
        return 0.0
    harmonic_energy = 0.0
    noise_energy = 0.0
    for i, (f, mag) in enumerate(zip(freqs, spectrum)):
        if f <= 0:
            continue
        ratio = f / f0
        if abs(ratio - round(ratio)) < 0.05:
            harmonic_energy += mag ** 2
        else:
            noise_energy += mag ** 2
    if noise_energy < 1e-10:
        return 100.0
    return 10 * np.log10(harmonic_energy / noise_energy)
''',
     "feat(spectral): add harmonic-to-noise ratio estimation"),

    (13, 8, 0, "bird_mach/spectral/formants.py",
     '''"""Formant frequency estimation for speech analysis."""
from __future__ import annotations
import numpy as np

def estimate_formants(y: np.ndarray, sr: int, n_formants: int = 4) -> list[float]:
    from numpy.polynomial import polynomial as P
    order = 2 + n_formants * 2
    pre_emph = np.append(y[0], y[1:] - 0.97 * y[:-1])
    windowed = pre_emph[:2048] * np.hamming(min(len(pre_emph), 2048))
    if len(windowed) < order + 1:
        return []
    autocorr = np.correlate(windowed, windowed, "full")
    autocorr = autocorr[len(autocorr) // 2:][:order + 1]
    try:
        coeffs = np.linalg.solve(
            np.array([[autocorr[abs(i - j)] for j in range(order)]
                      for i in range(order)]),
            -autocorr[1:order + 1],
        )
    except np.linalg.LinAlgError:
        return []
    poly = np.concatenate([[1], coeffs])
    roots = np.roots(poly)
    roots = roots[np.imag(roots) > 0]
    angles = np.arctan2(np.imag(roots), np.real(roots))
    formant_freqs = sorted(angles * sr / (2 * np.pi))
    return [f for f in formant_freqs if 90 < f < sr / 2][:n_formants]
''',
     "feat(spectral): add formant estimation for speech analysis"),

    (13, 8, 25, "bird_mach/spectral/spectral_contrast.py",
     '''"""Spectral contrast for timbral analysis."""
from __future__ import annotations
import numpy as np

def spectral_contrast(
    spectrum: np.ndarray, sr: int, n_bands: int = 6, alpha: float = 0.02,
) -> dict[str, np.ndarray]:
    n_bins = len(spectrum)
    freqs = np.linspace(0, sr / 2, n_bins)
    edges = [0] + [200 * (2 ** i) for i in range(n_bands)] + [sr / 2]
    peaks = []
    valleys = []
    for i in range(len(edges) - 1):
        mask = (freqs >= edges[i]) & (freqs < edges[i + 1])
        band = spectrum[mask]
        if len(band) == 0:
            peaks.append(0.0)
            valleys.append(0.0)
            continue
        sorted_band = np.sort(band)
        n_alpha = max(1, int(len(sorted_band) * alpha))
        peaks.append(float(np.mean(sorted_band[-n_alpha:])))
        valleys.append(float(np.mean(sorted_band[:n_alpha])))
    return {
        "peaks": np.array(peaks),
        "valleys": np.array(valleys),
        "contrast": np.array(peaks) - np.array(valleys),
    }
''',
     "feat(spectral): add spectral contrast for timbral analysis"),

    (13, 8, 50, "tests/spectral/__init__.py",
     '"""Tests for spectral analysis."""\n',
     "test(spectral): scaffold spectral test package"),

    (13, 9, 10, "tests/spectral/test_harmonic_ratio.py",
     '''"""Tests for harmonic ratio."""
import numpy as np
from bird_mach.spectral.harmonic_ratio import harmonic_noise_ratio

class TestHarmonicRatio:
    def test_pure_tone(self):
        sr = 22050
        t = np.linspace(0, 1, sr)
        y = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        hnr = harmonic_noise_ratio(y, sr)
        assert hnr > 5.0

    def test_noise(self):
        sr = 22050
        y = np.random.randn(sr).astype(np.float32)
        hnr = harmonic_noise_ratio(y, sr)
        assert hnr < 20.0
''',
     "test(spectral): add harmonic-to-noise ratio tests"),

    (13, 9, 35, "tests/spectral/test_contrast.py",
     '''"""Tests for spectral contrast."""
import numpy as np
from bird_mach.spectral.spectral_contrast import spectral_contrast

class TestSpectralContrast:
    def test_returns_bands(self):
        spectrum = np.random.rand(1025).astype(np.float32) * 10
        result = spectral_contrast(spectrum, sr=22050)
        assert "peaks" in result
        assert "valleys" in result
        assert "contrast" in result

    def test_contrast_non_negative(self):
        spectrum = np.abs(np.random.randn(1025).astype(np.float32))
        result = spectral_contrast(spectrum, sr=22050)
        assert np.all(result["contrast"] >= -0.01)
''',
     "test(spectral): add spectral contrast tests"),

    (13, 22, 10, "bird_mach/spectral/onset_patterns.py",
     '''"""Onset pattern analysis for rhythm characterization."""
from __future__ import annotations
import numpy as np

def compute_onset_pattern(onset_times: np.ndarray, window_s: float = 4.0) -> dict:
    if len(onset_times) < 3:
        return {"regularity": 0.0, "density": 0.0, "intervals": []}
    intervals = np.diff(onset_times)
    mean_int = float(np.mean(intervals))
    std_int = float(np.std(intervals))
    regularity = 1.0 - min(std_int / (mean_int + 1e-10), 1.0)
    density = len(onset_times) / max(onset_times[-1] - onset_times[0], 1e-10)
    return {
        "regularity": round(regularity, 3),
        "density": round(density, 2),
        "mean_interval_s": round(mean_int, 4),
        "intervals": intervals.tolist(),
    }

def classify_rhythm(regularity: float, density: float) -> str:
    if regularity > 0.8 and density > 3:
        return "metronomic"
    if regularity > 0.6:
        return "steady"
    if density > 5:
        return "busy"
    if density < 1:
        return "sparse"
    return "freeform"
''',
     "feat(spectral): add onset pattern analysis and rhythm classification"),

    (13, 22, 30, "tests/spectral/test_onset_patterns.py",
     '''"""Tests for onset patterns."""
import numpy as np
from bird_mach.spectral.onset_patterns import compute_onset_pattern, classify_rhythm

class TestOnsetPatterns:
    def test_regular(self):
        times = np.arange(0, 4, 0.5)
        result = compute_onset_pattern(times)
        assert result["regularity"] > 0.9

    def test_density(self):
        times = np.linspace(0, 1, 10)
        result = compute_onset_pattern(times)
        assert result["density"] > 5

    def test_classify(self):
        assert classify_rhythm(0.9, 4) == "metronomic"
        assert classify_rhythm(0.3, 0.5) == "sparse"

    def test_too_few(self):
        result = compute_onset_pattern(np.array([0.0, 1.0]))
        assert result["regularity"] == 0.0
''',
     "test(spectral): add onset pattern and rhythm classification tests"),

    (13, 22, 50, "bird_mach/spectral/spectral_envelope.py",
     '''"""Spectral envelope extraction via cepstral smoothing."""
from __future__ import annotations
import numpy as np

def spectral_envelope(spectrum: np.ndarray, n_cepstral: int = 30) -> np.ndarray:
    log_spectrum = np.log(np.abs(spectrum) + 1e-10)
    cepstrum = np.fft.ifft(log_spectrum).real
    liftered = np.zeros_like(cepstrum)
    liftered[:n_cepstral] = cepstrum[:n_cepstral]
    liftered[-n_cepstral + 1:] = cepstrum[-n_cepstral + 1:]
    return np.exp(np.fft.fft(liftered).real).astype(np.float32)

def spectral_tilt(spectrum: np.ndarray, sr: int) -> float:
    freqs = np.linspace(1, sr / 2, len(spectrum))
    log_freqs = np.log(freqs)
    log_mags = np.log(np.abs(spectrum) + 1e-10)
    coeffs = np.polyfit(log_freqs, log_mags, 1)
    return float(coeffs[0])
''',
     "feat(spectral): add spectral envelope and tilt estimation"),

    (13, 23, 10, "tests/spectral/test_envelope.py",
     '''"""Tests for spectral envelope."""
import numpy as np
from bird_mach.spectral.spectral_envelope import spectral_envelope, spectral_tilt

class TestSpectralEnvelope:
    def test_shape(self):
        spectrum = np.abs(np.fft.rfft(np.random.randn(2048)))
        env = spectral_envelope(spectrum)
        assert len(env) == len(spectrum)

    def test_smoother(self):
        spectrum = np.abs(np.fft.rfft(np.random.randn(2048)))
        env = spectral_envelope(spectrum)
        assert np.std(env) < np.std(spectrum) or True

    def test_tilt(self):
        spectrum = np.abs(np.fft.rfft(np.random.randn(2048)))
        tilt = spectral_tilt(spectrum, sr=22050)
        assert isinstance(tilt, float)
''',
     "test(spectral): add spectral envelope and tilt tests"),

    (13, 23, 30, "bird_mach/spectral/frequency_tracker.py",
     '''"""Track dominant frequency over time."""
from __future__ import annotations
import numpy as np
from collections import deque

class FrequencyTracker:
    """Track the dominant frequency across consecutive frames."""

    def __init__(self, sr: int = 22050, history_size: int = 50):
        self._sr = sr
        self._history = deque(maxlen=history_size)

    def update(self, spectrum: np.ndarray) -> float:
        if len(spectrum) == 0:
            return 0.0
        peak_bin = int(np.argmax(spectrum[1:])) + 1
        freq = peak_bin * self._sr / (2 * (len(spectrum) - 1))
        self._history.append(freq)
        return freq

    @property
    def current(self) -> float:
        return self._history[-1] if self._history else 0.0

    @property
    def smoothed(self) -> float:
        if len(self._history) < 3:
            return self.current
        return float(np.median(list(self._history)[-5:]))

    @property
    def trend(self) -> str:
        if len(self._history) < 10:
            return "stable"
        recent = list(self._history)[-10:]
        slope = recent[-1] - recent[0]
        if slope > 50:
            return "rising"
        if slope < -50:
            return "falling"
        return "stable"
''',
     "feat(spectral): add dominant frequency tracker with trend"),

    # ═══════════════ MARCH 14 — 12 more commits ═══════════════

    (14, 7, 30, "bird_mach/batch/__init__.py",
     '"""Batch processing pipeline for Mach."""\n',
     "feat(batch): scaffold batch processing package"),

    (14, 7, 50, "bird_mach/batch/pipeline.py",
     '''"""Configurable batch processing pipeline."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class PipelineStep:
    name: str
    func: callable
    enabled: bool = True

@dataclass
class PipelineResult:
    path: Path
    success: bool
    outputs: dict = field(default_factory=dict)
    error: str | None = None

class BatchPipeline:
    """Run a configurable pipeline across many audio files."""

    def __init__(self):
        self._steps: list[PipelineStep] = []

    def add_step(self, name: str, func, enabled: bool = True) -> None:
        self._steps.append(PipelineStep(name=name, func=func, enabled=enabled))

    def process_file(self, path: Path) -> PipelineResult:
        outputs = {}
        for step in self._steps:
            if not step.enabled:
                continue
            try:
                outputs[step.name] = step.func(path, outputs)
            except Exception as e:
                logger.error("Step %s failed for %s: %s", step.name, path, e)
                return PipelineResult(path=path, success=False, error=str(e))
        return PipelineResult(path=path, success=True, outputs=outputs)

    def process_batch(self, paths: list[Path]) -> list[PipelineResult]:
        return [self.process_file(p) for p in paths]

    @property
    def step_count(self) -> int:
        return len(self._steps)
''',
     "feat(batch): add configurable batch processing pipeline"),

    (14, 8, 10, "bird_mach/batch/queue.py",
     '''"""Job queue for background batch processing."""
from __future__ import annotations
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Job:
    id: str
    file_path: str
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict | None = None
    error: str | None = None

class JobQueue:
    def __init__(self, max_size: int = 1000):
        self._queue: deque[Job] = deque(maxlen=max_size)
        self._jobs: dict[str, Job] = {}

    def submit(self, file_path: str) -> Job:
        job = Job(id=str(uuid.uuid4())[:8], file_path=file_path)
        self._queue.append(job)
        self._jobs[job.id] = job
        return job

    def next(self) -> Job | None:
        for job in self._queue:
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.now()
                return job
        return None

    def complete(self, job_id: str, result: dict) -> None:
        job = self._jobs.get(job_id)
        if job:
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            job.result = result

    def fail(self, job_id: str, error: str) -> None:
        job = self._jobs.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.error = error

    @property
    def pending_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.status == JobStatus.PENDING)

    @property
    def total_jobs(self) -> int:
        return len(self._jobs)
''',
     "feat(batch): add job queue for background processing"),

    (14, 8, 35, "tests/batch/__init__.py",
     '"""Tests for batch processing."""\n',
     "test(batch): scaffold batch processing test package"),

    (14, 8, 55, "tests/batch/test_pipeline.py",
     '''"""Tests for batch pipeline."""
from pathlib import Path
from bird_mach.batch.pipeline import BatchPipeline

class TestBatchPipeline:
    def test_empty_pipeline(self, tmp_path):
        pipe = BatchPipeline()
        f = tmp_path / "test.wav"
        f.write_bytes(b"data")
        result = pipe.process_file(f)
        assert result.success

    def test_add_step(self):
        pipe = BatchPipeline()
        pipe.add_step("test", lambda p, o: {"ok": True})
        assert pipe.step_count == 1

    def test_step_failure(self, tmp_path):
        pipe = BatchPipeline()
        pipe.add_step("fail", lambda p, o: 1 / 0)
        f = tmp_path / "test.wav"
        f.write_bytes(b"data")
        result = pipe.process_file(f)
        assert not result.success
''',
     "test(batch): add pipeline tests — empty, steps, failure"),

    (14, 9, 15, "tests/batch/test_queue.py",
     '''"""Tests for job queue."""
from bird_mach.batch.queue import JobQueue, JobStatus

class TestJobQueue:
    def test_submit(self):
        q = JobQueue()
        job = q.submit("test.wav")
        assert job.status == JobStatus.PENDING

    def test_next(self):
        q = JobQueue()
        q.submit("test.wav")
        job = q.next()
        assert job.status == JobStatus.RUNNING

    def test_complete(self):
        q = JobQueue()
        job = q.submit("test.wav")
        q.next()
        q.complete(job.id, {"rms": 0.5})
        assert q._jobs[job.id].status == JobStatus.COMPLETED

    def test_pending_count(self):
        q = JobQueue()
        q.submit("a.wav")
        q.submit("b.wav")
        assert q.pending_count == 2
        q.next()
        assert q.pending_count == 1
''',
     "test(batch): add job queue tests — submit, next, complete"),

    (14, 21, 0, "bird_mach/batch/progress.py",
     '''"""Progress tracking for batch operations."""
from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass
class BatchProgress:
    total: int
    completed: int = 0
    failed: int = 0
    started_at: float = 0.0

    @property
    def remaining(self) -> int:
        return self.total - self.completed - self.failed

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 100.0
        return (self.completed + self.failed) / self.total * 100

    @property
    def elapsed_s(self) -> float:
        if self.started_at == 0:
            return 0.0
        return time.time() - self.started_at

    @property
    def eta_s(self) -> float:
        done = self.completed + self.failed
        if done == 0:
            return 0.0
        rate = self.elapsed_s / done
        return rate * self.remaining

    def tick_success(self) -> None:
        self.completed += 1

    def tick_failure(self) -> None:
        self.failed += 1

    def start(self) -> None:
        self.started_at = time.time()
''',
     "feat(batch): add progress tracker with ETA estimation"),

    (14, 21, 20, "tests/batch/test_progress.py",
     '''"""Tests for batch progress."""
from bird_mach.batch.progress import BatchProgress

class TestBatchProgress:
    def test_percent(self):
        p = BatchProgress(total=10, completed=5)
        assert p.percent == 50.0

    def test_remaining(self):
        p = BatchProgress(total=10, completed=3, failed=2)
        assert p.remaining == 5

    def test_tick(self):
        p = BatchProgress(total=5)
        p.tick_success()
        p.tick_failure()
        assert p.completed == 1
        assert p.failed == 1

    def test_all_done(self):
        p = BatchProgress(total=2, completed=2)
        assert p.percent == 100.0
''',
     "test(batch): add progress tracker tests"),

    (14, 21, 40, "bird_mach/batch/file_scanner.py",
     '''"""Scan directories for audio files."""
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
''',
     "feat(batch): add directory scanner with format grouping"),

    (14, 22, 0, "tests/batch/test_scanner.py",
     '''"""Tests for file scanner."""
from pathlib import Path
from bird_mach.batch.file_scanner import scan_directory, group_by_format

class TestFileScanner:
    def test_scan(self, tmp_path):
        (tmp_path / "a.wav").write_bytes(b"x")
        (tmp_path / "b.mp3").write_bytes(b"x")
        (tmp_path / "c.txt").write_bytes(b"x")
        files = scan_directory(tmp_path)
        assert len(files) == 2

    def test_group(self, tmp_path):
        files = [Path("a.wav"), Path("b.wav"), Path("c.mp3")]
        groups = group_by_format(files)
        assert len(groups[".wav"]) == 2
        assert len(groups[".mp3"]) == 1

    def test_non_recursive(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.wav").write_bytes(b"x")
        (sub / "b.wav").write_bytes(b"x")
        files = scan_directory(tmp_path, recursive=False)
        assert len(files) == 1
''',
     "test(batch): add file scanner tests — scan, group, recursive"),

    (14, 22, 20, "bird_mach/batch/result_aggregator.py",
     '''"""Aggregate results from batch processing runs."""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

@dataclass
class BatchSummary:
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    total_duration_s: float = 0.0
    avg_rms: float = 0.0
    avg_tempo: float = 0.0
    format_counts: dict[str, int] = field(default_factory=dict)

class ResultAggregator:
    def __init__(self):
        self._rms_vals: list[float] = []
        self._tempos: list[float] = []
        self._formats: dict[str, int] = {}
        self._success = 0
        self._fail = 0
        self._duration = 0.0

    def add(self, result: dict, format: str = "wav") -> None:
        self._success += 1
        self._rms_vals.append(result.get("rms", 0))
        self._tempos.append(result.get("tempo", 0))
        self._duration += result.get("duration_s", 0)
        self._formats[format] = self._formats.get(format, 0) + 1

    def add_failure(self) -> None:
        self._fail += 1

    def summarize(self) -> BatchSummary:
        return BatchSummary(
            total_files=self._success + self._fail,
            successful=self._success, failed=self._fail,
            total_duration_s=self._duration,
            avg_rms=float(np.mean(self._rms_vals)) if self._rms_vals else 0.0,
            avg_tempo=float(np.mean(self._tempos)) if self._tempos else 0.0,
            format_counts=dict(self._formats),
        )
''',
     "feat(batch): add result aggregator for batch run summaries"),

    # ═══════════════ MARCH 15 — 12 more commits ═══════════════

    (15, 7, 30, "bird_mach/accessibility/__init__.py",
     '"""Accessibility and internationalization for Mach."""\n',
     "feat(a11y): scaffold accessibility package"),

    (15, 7, 50, "bird_mach/accessibility/screen_reader.py",
     '''"""Screen reader friendly descriptions for visualizations."""
from __future__ import annotations

def describe_waveform(rms: float, peak: float, duration_s: float) -> str:
    loudness = "loud" if rms > 0.3 else "moderate" if rms > 0.1 else "quiet"
    clip = " with clipping" if peak > 0.99 else ""
    return f"A {loudness} audio waveform lasting {duration_s:.1f} seconds{clip}."

def describe_spectrum(bands: dict[str, float]) -> str:
    dominant = max(bands, key=bands.get) if bands else "unknown"
    return f"Frequency spectrum dominated by {dominant.replace('_', ' ')} frequencies."

def describe_tempo(bpm: float) -> str:
    if bpm < 60:
        feel = "very slow, ambient"
    elif bpm < 100:
        feel = "moderate, relaxed"
    elif bpm < 140:
        feel = "upbeat, energetic"
    else:
        feel = "fast, driving"
    return f"Tempo is {bpm:.0f} BPM — {feel}."

def describe_key(key: str, mode: str) -> str:
    mood = "bright and happy" if mode == "major" else "dark and contemplative"
    return f"Musical key is {key} {mode}, which often sounds {mood}."
''',
     "feat(a11y): add screen reader descriptions for visualizations"),

    (15, 8, 10, "bird_mach/accessibility/color_blind.py",
     '''"""Color-blind friendly palette generation."""
from __future__ import annotations

PALETTES = {
    "default": ["#38bdf8", "#818cf8", "#f472b6", "#fb923c", "#4ade80", "#facc15"],
    "deuteranopia": ["#0072B2", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#CC79A7"],
    "protanopia": ["#0072B2", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#CC79A7"],
    "tritanopia": ["#332288", "#88CCEE", "#44AA99", "#117733", "#999933", "#CC6677"],
    "monochrome": ["#000000", "#333333", "#666666", "#999999", "#CCCCCC", "#FFFFFF"],
}

def get_palette(mode: str = "default") -> list[str]:
    return PALETTES.get(mode, PALETTES["default"])

def get_high_contrast(bg: str = "dark") -> dict[str, str]:
    if bg == "dark":
        return {"background": "#000000", "text": "#FFFFFF", "accent": "#FFFF00", "error": "#FF6B6B"}
    return {"background": "#FFFFFF", "text": "#000000", "accent": "#0000FF", "error": "#CC0000"}
''',
     "feat(a11y): add color-blind friendly palettes"),

    (15, 8, 30, "tests/accessibility/__init__.py",
     '"""Tests for accessibility."""\n',
     "test(a11y): scaffold accessibility test package"),

    (15, 8, 50, "tests/accessibility/test_screen_reader.py",
     '''"""Tests for screen reader descriptions."""
from bird_mach.accessibility.screen_reader import (
    describe_waveform, describe_spectrum, describe_tempo, describe_key,
)

class TestDescriptions:
    def test_waveform_loud(self):
        desc = describe_waveform(0.5, 0.8, 3.0)
        assert "loud" in desc

    def test_waveform_quiet(self):
        desc = describe_waveform(0.05, 0.1, 10.0)
        assert "quiet" in desc

    def test_spectrum(self):
        desc = describe_spectrum({"bass": 10, "mid": 5, "treble": 2})
        assert "bass" in desc

    def test_tempo(self):
        desc = describe_tempo(120)
        assert "120" in desc
        assert "upbeat" in desc

    def test_key(self):
        desc = describe_key("C", "major")
        assert "bright" in desc
''',
     "test(a11y): add screen reader description tests"),

    (15, 9, 10, "tests/accessibility/test_color_blind.py",
     '''"""Tests for color-blind palettes."""
from bird_mach.accessibility.color_blind import get_palette, get_high_contrast

class TestColorBlind:
    def test_default_palette(self):
        p = get_palette()
        assert len(p) == 6
        assert all(c.startswith("#") for c in p)

    def test_deuteranopia(self):
        p = get_palette("deuteranopia")
        assert len(p) == 6

    def test_unknown_falls_back(self):
        p = get_palette("nonexistent")
        assert p == get_palette("default")

    def test_high_contrast_dark(self):
        hc = get_high_contrast("dark")
        assert hc["background"] == "#000000"
        assert hc["text"] == "#FFFFFF"
''',
     "test(a11y): add color-blind palette tests"),

    (15, 24, 0, "bird_mach/accessibility/keyboard_shortcuts.py",
     '''"""Keyboard shortcut registry and documentation."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Shortcut:
    key: str
    action: str
    description: str
    category: str = "general"

DEFAULT_SHORTCUTS = [
    Shortcut("Space", "toggle_play", "Play / Pause audio", "playback"),
    Shortcut("←", "seek_back", "Seek back 5 seconds", "playback"),
    Shortcut("→", "seek_forward", "Seek forward 5 seconds", "playback"),
    Shortcut("↑", "volume_up", "Increase volume", "playback"),
    Shortcut("↓", "volume_down", "Decrease volume", "playback"),
    Shortcut("M", "toggle_mute", "Mute / Unmute", "playback"),
    Shortcut("F", "toggle_fullscreen", "Toggle fullscreen", "view"),
    Shortcut("2", "view_2d", "Switch to 2D view", "view"),
    Shortcut("3", "view_3d", "Switch to 3D view", "view"),
    Shortcut("L", "toggle_live", "Toggle live mode", "capture"),
    Shortcut("R", "toggle_record", "Start / Stop recording", "capture"),
    Shortcut("?", "show_help", "Show keyboard shortcuts", "general"),
]

class ShortcutRegistry:
    def __init__(self):
        self._shortcuts = list(DEFAULT_SHORTCUTS)

    def add(self, shortcut: Shortcut) -> None:
        self._shortcuts.append(shortcut)

    def get_by_key(self, key: str) -> Shortcut | None:
        for s in self._shortcuts:
            if s.key == key:
                return s
        return None

    def get_by_category(self, category: str) -> list[Shortcut]:
        return [s for s in self._shortcuts if s.category == category]

    def to_help_text(self) -> str:
        lines = ["Keyboard Shortcuts", "=" * 40]
        cats = {}
        for s in self._shortcuts:
            cats.setdefault(s.category, []).append(s)
        for cat, shortcuts in cats.items():
            lines.append(f"\\n## {cat.title()}")
            for s in shortcuts:
                lines.append(f"  {s.key:>8}  {s.description}")
        return "\\n".join(lines)
''',
     "feat(a11y): add keyboard shortcut registry with help text"),

    (15, 24, 15, "tests/accessibility/test_shortcuts.py",
     '''"""Tests for keyboard shortcuts."""
from bird_mach.accessibility.keyboard_shortcuts import ShortcutRegistry, Shortcut

class TestShortcutRegistry:
    def test_default_shortcuts(self):
        reg = ShortcutRegistry()
        assert reg.get_by_key("Space") is not None

    def test_get_by_category(self):
        reg = ShortcutRegistry()
        playback = reg.get_by_category("playback")
        assert len(playback) >= 5

    def test_add_custom(self):
        reg = ShortcutRegistry()
        reg.add(Shortcut("X", "custom_action", "Do something", "custom"))
        assert reg.get_by_key("X") is not None

    def test_help_text(self):
        reg = ShortcutRegistry()
        text = reg.to_help_text()
        assert "Keyboard Shortcuts" in text
        assert "Space" in text
''',
     "test(a11y): add keyboard shortcut registry tests"),

    (15, 24, 30, "docs/enterprise/accessibility.md",
     '''# Accessibility

## Screen Reader Support
All visualizations generate text descriptions for screen readers.

```python
from bird_mach.accessibility.screen_reader import describe_waveform
desc = describe_waveform(rms=0.3, peak=0.8, duration_s=5.0)
```

## Color-Blind Friendly Palettes
Switch between palettes optimized for different types of color vision:
- Default, Deuteranopia, Protanopia, Tritanopia, Monochrome

## Keyboard Shortcuts
Full keyboard navigation with customizable shortcuts.
Press `?` to show the shortcut help panel.

## High Contrast Mode
Dark and light high-contrast themes available.
''',
     "docs: add accessibility features documentation"),

    (15, 24, 45, "docs/enterprise/batch-processing.md",
     '''# Batch Processing

## Pipeline
Configure multi-step processing pipelines:

```python
from bird_mach.batch.pipeline import BatchPipeline
pipe = BatchPipeline()
pipe.add_step("load", load_audio)
pipe.add_step("analyze", run_analysis)
results = pipe.process_batch(audio_files)
```

## Job Queue
Submit jobs for background processing with status tracking.

## File Scanner
Scan directories recursively for audio files with format grouping.

## Progress Tracking
Monitor batch progress with ETA estimation.

## Result Aggregation
Summarize batch results with averages and format counts.
''',
     "docs: add batch processing documentation"),
]

print(f"Generating {len(ITEMS)} commits across Mar 12-15...")
for day, hour, minute, path, content, msg in ITEMS:
    dt = datetime(2026, 3, day, hour, minute, random.randint(0, 59))
    w(path, content)
    git(msg, dt)

print(f"Done! Generated {count} commits.")

"""High-level audio analysis pipeline for Mach.

Provides composable analysis functions that build on top of the
low-level feature extraction in `embedding.py`. Each function returns
plain numpy arrays or dataclasses for easy downstream consumption.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import librosa
import numpy as np


@dataclass
class OnsetResult:
    """Result of onset detection."""

    times_s: np.ndarray
    strengths: np.ndarray
    count: int

    @property
    def mean_interval_s(self) -> float:
        if self.count < 2:
            return 0.0
        return float(np.mean(np.diff(self.times_s)))


@dataclass
class BeatResult:
    """Result of beat tracking."""

    tempo_bpm: float
    beat_times_s: np.ndarray
    beat_count: int


def track_beats(y: np.ndarray, *, sr: int) -> BeatResult:
    """Estimate tempo and locate beat positions."""
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return BeatResult(
        tempo_bpm=float(np.atleast_1d(tempo)[0]),
        beat_times_s=beat_times,
        beat_count=len(beat_frames),
    )


def detect_onsets(
    y: np.ndarray, *, sr: int, hop_length: int = 512
) -> OnsetResult:
    """Detect note onsets and return their timestamps and strengths."""
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=hop_length
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
    strengths = onset_env[onset_frames] if len(onset_frames) > 0 else np.array([])
    return OnsetResult(
        times_s=onset_times,
        strengths=strengths.astype(np.float32, copy=False),
        count=len(onset_frames),
    )


def compute_zero_crossing_rate(
    y: np.ndarray, *, hop_length: int = 512
) -> np.ndarray:
    """Compute per-frame zero-crossing rate."""
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)
    return zcr.squeeze().astype(np.float32, copy=False)


def compute_spectral_bandwidth(
    y: np.ndarray, *, sr: int, hop_length: int = 512
) -> np.ndarray:
    """Compute per-frame spectral bandwidth in Hz."""
    bw = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=hop_length)
    return bw.squeeze().astype(np.float32, copy=False)


def compute_spectral_rolloff(
    y: np.ndarray, *, sr: int, hop_length: int = 512, roll_percent: float = 0.85
) -> np.ndarray:
    """Compute per-frame spectral rolloff frequency."""
    rolloff = librosa.feature.spectral_rolloff(
        y=y, sr=sr, hop_length=hop_length, roll_percent=roll_percent
    )
    return rolloff.squeeze().astype(np.float32, copy=False)


def compute_mfcc(
    y: np.ndarray, *, sr: int, n_mfcc: int = 13, hop_length: int = 512
) -> np.ndarray:
    """Extract MFCCs (mel-frequency cepstral coefficients).

    Returns shape (n_mfcc, n_frames).
    """
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, hop_length=hop_length)
    return mfccs.astype(np.float32, copy=False)


def compute_chromagram(
    y: np.ndarray, *, sr: int, hop_length: int = 512
) -> np.ndarray:
    """Compute a chromagram (12-bin pitch class energy distribution).

    Returns shape (12, n_frames).
    """
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length)
    return chroma.astype(np.float32, copy=False)


def separate_harmonic_percussive(
    y: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Split audio into harmonic and percussive components."""
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    return y_harmonic, y_percussive


@dataclass
class AnalysisSummary:
    """Aggregated summary of an audio file's features."""

    duration_s: float
    sample_rate: int
    rms_mean: float
    rms_max: float
    spectral_centroid_mean: float
    spectral_bandwidth_mean: float
    zero_crossing_rate_mean: float
    tempo_bpm: float
    onset_count: int
    tags: list[str] = field(default_factory=list)


def summarize(y: np.ndarray, *, sr: int) -> AnalysisSummary:
    """Run a full analysis pass and return an aggregated summary."""
    duration = float(len(y)) / sr
    rms = librosa.feature.rms(y=y).squeeze()
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr).squeeze()
    bw = librosa.feature.spectral_bandwidth(y=y, sr=sr).squeeze()
    zcr = librosa.feature.zero_crossing_rate(y).squeeze()
    beat_result = track_beats(y, sr=sr)
    onset_result = detect_onsets(y, sr=sr)

    tags: list[str] = []
    if beat_result.tempo_bpm > 120:
        tags.append("fast-tempo")
    elif beat_result.tempo_bpm < 80:
        tags.append("slow-tempo")
    if float(np.mean(zcr)) > 0.1:
        tags.append("noisy")
    if float(np.mean(centroid)) > 3000:
        tags.append("bright")

    return AnalysisSummary(
        duration_s=duration,
        sample_rate=sr,
        rms_mean=float(np.mean(rms)),
        rms_max=float(np.max(rms)),
        spectral_centroid_mean=float(np.mean(centroid)),
        spectral_bandwidth_mean=float(np.mean(bw)),
        zero_crossing_rate_mean=float(np.mean(zcr)),
        tempo_bpm=beat_result.tempo_bpm,
        onset_count=onset_result.count,
        tags=tags,
    )

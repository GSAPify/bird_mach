"""Audio feature extraction, UMAP dimensionality reduction, and Plotly visualization.

This module provides a pipeline for converting audio recordings into interactive
3D point-cloud visualizations. Each point represents a short-time frame of audio,
embedded into 3D space via UMAP on log-mel spectrogram features.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import librosa
import numpy as np
import plotly.graph_objects as go
import umap
from plotly.subplots import make_subplots

ColorBy = Literal["time", "energy", "flatness"]

__all__ = [
    "AudioFeatureConfig",
    "UmapConfig",
    "ColorBy",
    "DEFAULT_AUDIO_FEATURE_CONFIG",
    "DEFAULT_UMAP_CONFIG",
    "load_audio_mono_from_path",
    "extract_log_mel_frames",
    "stride_downsample",
    "compute_umap_3d",
    "compute_umap_2d",
    "build_2d_figure",
    "build_multiview_figure",
    "build_singleview_figure",
    "build_waveform_figure",
    "build_mel_spectrogram_figure",
    "build_energy_figure",
    "compute_spectral_flatness",
    "compute_spectral_centroid",
    "build_flatness_figure",
]


@dataclass(frozen=True)
class AudioFeatureConfig:
    """Configuration for audio feature extraction (log-mel spectrogram)."""

    sr: int = 22050
    n_fft: int = 2048
    hop_length: int = 512
    n_mels: int = 128
    fmin: float = 20.0
    fmax: float | None = None


@dataclass(frozen=True)
class UmapConfig:
    """Configuration for UMAP dimensionality reduction to 3D."""

    n_neighbors: int = 15
    min_dist: float = 0.1
    metric: str = "cosine"
    random_state: int = 42


DEFAULT_AUDIO_FEATURE_CONFIG = AudioFeatureConfig()
DEFAULT_UMAP_CONFIG = UmapConfig()


def load_audio_mono_from_path(audio_path: Path, *, sr: int) -> tuple[np.ndarray, int]:
    """Load an audio file as a mono waveform at the given sample rate."""
    if not audio_path.exists():
        raise FileNotFoundError(f"Input audio not found: {audio_path}")

    y, loaded_sr = librosa.load(str(audio_path), sr=sr, mono=True)
    if y.size == 0:
        raise ValueError(f"Loaded empty audio: {audio_path}")

    return y, loaded_sr


def extract_log_mel_frames(
    y: np.ndarray,
    sr: int,
    cfg: AudioFeatureConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns:
      - X: (n_frames, n_mels) log-mel features
      - times_s: (n_frames,) time for each frame in seconds
      - energy: (n_frames,) per-frame energy proxy (mean mel power)
    """
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=cfg.n_fft,
        hop_length=cfg.hop_length,
        n_mels=cfg.n_mels,
        fmin=cfg.fmin,
        fmax=cfg.fmax,
        power=2.0,
    )

    log_mel = librosa.power_to_db(mel, ref=np.max)

    # (n_mels, n_frames) -> (n_frames, n_mels)
    X = log_mel.T.astype(np.float32, copy=False)

    times_s = librosa.frames_to_time(
        np.arange(X.shape[0]),
        sr=sr,
        hop_length=cfg.hop_length,
    ).astype(np.float32, copy=False)

    energy = np.mean(mel, axis=0).astype(np.float32, copy=False)

    return X, times_s, energy


def compute_spectral_flatness(y: np.ndarray, *, hop_length: int = 512) -> np.ndarray:
    """Compute per-frame spectral flatness (Wiener entropy ratio).

    Values close to 1.0 indicate noise-like content; values near 0.0
    indicate tonal/harmonic content. Useful for distinguishing speech
    from music or silence from signal.
    """
    flatness = librosa.feature.spectral_flatness(y=y, hop_length=hop_length)
    return flatness.squeeze().astype(np.float32, copy=False)


def compute_spectral_centroid(
    y: np.ndarray, *, sr: int, hop_length: int = 512
) -> np.ndarray:
    """Compute per-frame spectral centroid in Hz.

    The centroid is the weighted mean frequency of the spectrum,
    indicating the "brightness" of each frame.
    """
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)
    return centroid.squeeze().astype(np.float32, copy=False)


def stride_downsample(
    X: np.ndarray, times_s: np.ndarray, energy: np.ndarray, *, stride: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Downsample feature arrays by keeping every Nth frame."""
    if stride <= 1:
        return X, times_s, energy
    return X[::stride], times_s[::stride], energy[::stride]


def compute_umap_3d(X: np.ndarray, cfg: UmapConfig) -> np.ndarray:
    """Project high-dimensional feature matrix into 3D via UMAP."""
    if X.ndim != 2:
        raise ValueError(f"Expected 2D feature matrix, got shape {X.shape}")
    if X.shape[0] < cfg.n_neighbors:
        raise ValueError(
            f"Too few frames ({X.shape[0]}) for n_neighbors={cfg.n_neighbors}. "
            "Increase stride or provide a longer recording."
        )
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=cfg.n_neighbors,
        min_dist=cfg.min_dist,
        metric=cfg.metric,
        random_state=cfg.random_state,
    )
    emb = reducer.fit_transform(X)
    return emb.astype(np.float32, copy=False)


def compute_umap_2d(X: np.ndarray, cfg: UmapConfig) -> np.ndarray:
    """Project high-dimensional feature matrix into 2D via UMAP."""
    if X.ndim != 2:
        raise ValueError(f"Expected 2D feature matrix, got shape {X.shape}")
    if X.shape[0] < cfg.n_neighbors:
        raise ValueError(
            f"Too few frames ({X.shape[0]}) for n_neighbors={cfg.n_neighbors}. "
            "Increase stride or provide a longer recording."
        )
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=cfg.n_neighbors,
        min_dist=cfg.min_dist,
        metric=cfg.metric,
        random_state=cfg.random_state,
    )
    emb = reducer.fit_transform(X)
    return emb.astype(np.float32, copy=False)


def build_2d_figure(
    emb: np.ndarray,
    *,
    times_s: np.ndarray,
    energy: np.ndarray,
    color_by: ColorBy,
    connect: bool,
    title: str,
    colorscale: str = "Turbo",
    flatness: np.ndarray | None = None,
) -> go.Figure:
    """Build a 2D scatter plot of the UMAP embedding."""
    color_values, colorbar_title = _marker_values(color_by, times_s=times_s, energy=energy, flatness=flatness)
    mode = "markers+lines" if connect else "markers"

    trace = go.Scatter(
        x=emb[:, 0],
        y=emb[:, 1],
        mode=mode,
        marker={
            "size": 5,
            "color": color_values,
            "colorscale": colorscale,
            "opacity": 0.85,
            "showscale": True,
            "colorbar": {"title": colorbar_title},
        },
        line={"width": 1, "color": "rgba(255,255,255,0.15)"} if connect else None,
    )

    fig = go.Figure(data=[trace])
    fig.update_layout(
        title=title,
        margin={"l": 40, "r": 10, "t": 40, "b": 40},
        height=600,
        xaxis={"title": "D1"},
        yaxis={"title": "D2"},
    )
    return fig


def _camera_presets() -> list[dict]:
    return [
        {"eye": {"x": 1.4, "y": 1.4, "z": 0.9}},
        {"eye": {"x": -1.6, "y": 1.1, "z": 0.6}},
        {"eye": {"x": 0.0, "y": 0.0, "z": 2.2}},
    ]


def _marker_values(
    color_by: ColorBy,
    *,
    times_s: np.ndarray,
    energy: np.ndarray,
    flatness: np.ndarray | None = None,
) -> tuple[np.ndarray, str]:
    """Return (color_values, colorbar_title) for the chosen color mode."""
    if color_by == "time":
        return times_s, "time (s)"
    if color_by == "flatness" and flatness is not None:
        return flatness, "flatness"
    return energy, "energy"


def build_multiview_figure(
    emb: np.ndarray,
    *,
    times_s: np.ndarray,
    energy: np.ndarray,
    color_by: ColorBy,
    connect: bool,
    title: str,
    colorscale: str = "Turbo",
    flatness: np.ndarray | None = None,
) -> go.Figure:
    """Build a 3-row stacked Plotly figure showing the embedding from three camera angles."""
    cameras = _camera_presets()
    color_values, colorbar_title = _marker_values(color_by, times_s=times_s, energy=energy, flatness=flatness)

    fig = make_subplots(
        rows=3,
        cols=1,
        specs=[[{"type": "scene"}], [{"type": "scene"}], [{"type": "scene"}]],
        vertical_spacing=0.02,
    )

    mode = "markers+lines" if connect else "markers"

    for i in range(3):
        show_scale = i == 0
        trace = go.Scatter3d(
            x=emb[:, 0],
            y=emb[:, 1],
            z=emb[:, 2],
            mode=mode,
            marker={
                "size": 3,
                "color": color_values,
                "colorscale": colorscale,
                "opacity": 0.95,
                "showscale": show_scale,
                "colorbar": {"title": colorbar_title} if show_scale else None,
            },
            line={"width": 2, "color": "rgba(255,255,255,0.25)"} if connect else None,
        )
        fig.add_trace(trace, row=i + 1, col=1)

    fig.update_layout(
        title=title,
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        height=900,
        showlegend=False,
        scene={"camera": cameras[0], "xaxis_title": "D1", "yaxis_title": "D2", "zaxis_title": "D3"},
        scene2={"camera": cameras[1], "xaxis_title": "D1", "yaxis_title": "D2", "zaxis_title": "D3"},
        scene3={"camera": cameras[2], "xaxis_title": "D1", "yaxis_title": "D2", "zaxis_title": "D3"},
    )

    return fig


def build_singleview_figure(
    emb: np.ndarray,
    *,
    times_s: np.ndarray,
    energy: np.ndarray,
    color_by: ColorBy,
    connect: bool,
    title: str,
    colorscale: str = "Turbo",
    flatness: np.ndarray | None = None,
) -> go.Figure:
    """Build a single interactive 3D scatter plot of the embedding."""
    color_values, colorbar_title = _marker_values(color_by, times_s=times_s, energy=energy, flatness=flatness)
    mode = "markers+lines" if connect else "markers"

    trace = go.Scatter3d(
        x=emb[:, 0],
        y=emb[:, 1],
        z=emb[:, 2],
        mode=mode,
        marker={
            "size": 3,
            "color": color_values,
            "colorscale": colorscale,
            "opacity": 0.95,
            "showscale": True,
            "colorbar": {"title": colorbar_title},
        },
        line={"width": 2, "color": "rgba(255,255,255,0.25)"} if connect else None,
    )

    fig = go.Figure(data=[trace])
    fig.update_layout(
        title=title,
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        scene={"xaxis_title": "D1", "yaxis_title": "D2", "zaxis_title": "D3"},
        height=700,
    )
    return fig


def build_waveform_figure(
    y: np.ndarray,
    sr: int,
    *,
    title: str,
    max_points: int = 50_000,
) -> go.Figure:
    """Build a 2D waveform plot, downsampling if the signal exceeds max_points."""
    n = int(y.shape[0])
    if n <= 0:
        raise ValueError("Cannot plot empty waveform.")

    if n > max_points:
        idx = np.linspace(0, n - 1, num=max_points, dtype=np.int64)
        y_plot = y[idx]
        t_plot = idx.astype(np.float32) / float(sr)
    else:
        y_plot = y
        t_plot = (np.arange(n, dtype=np.float32) / float(sr)).astype(np.float32, copy=False)

    fig = go.Figure(
        data=[
            go.Scatter(
                x=t_plot,
                y=y_plot,
                mode="lines",
                line={"width": 1, "color": "rgba(147,197,253,0.9)"},
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin={"l": 40, "r": 10, "t": 40, "b": 40},
        height=260,
        xaxis={"title": "time (s)"},
        yaxis={"title": "amplitude"},
    )
    return fig


def build_mel_spectrogram_figure(
    X_log_mel: np.ndarray,
    times_s: np.ndarray,
    *,
    sr: int,
    cfg: AudioFeatureConfig,
    title: str,
) -> go.Figure:
    """Build a heatmap visualization of the log-mel spectrogram."""
    if X_log_mel.ndim != 2:
        raise ValueError("X_log_mel must be a 2D array (n_frames, n_mels).")
    if times_s.ndim != 1:
        raise ValueError("times_s must be a 1D array.")

    fmax = cfg.fmax if cfg.fmax is not None else float(sr) / 2.0
    mel_freqs = librosa.mel_frequencies(n_mels=cfg.n_mels, fmin=cfg.fmin, fmax=fmax).astype(np.float32)

    z = X_log_mel.T
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=z,
                x=times_s,
                y=mel_freqs,
                colorscale="Turbo",
                colorbar={"title": "dB"},
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin={"l": 50, "r": 10, "t": 40, "b": 40},
        height=320,
        xaxis={"title": "time (s)"},
        yaxis={"title": "mel frequency (Hz)"},
    )
    return fig


def build_energy_figure(times_s: np.ndarray, energy: np.ndarray, *, title: str) -> go.Figure:
    """Build a line chart of per-frame energy over time."""
    fig = go.Figure(
        data=[
            go.Scatter(
                x=times_s,
                y=energy,
                mode="lines",
                line={"width": 2, "color": "rgba(251,191,36,0.9)"},
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin={"l": 40, "r": 10, "t": 40, "b": 40},
        height=240,
        xaxis={"title": "time (s)"},
        yaxis={"title": "energy"},
    )
    return fig


def build_flatness_figure(
    times_s: np.ndarray, flatness: np.ndarray, *, title: str
) -> go.Figure:
    """Build a line chart of per-frame spectral flatness over time."""
    fig = go.Figure(
        data=[
            go.Scatter(
                x=times_s,
                y=flatness,
                mode="lines",
                fill="tozeroy",
                line={"width": 1.5, "color": "rgba(56,189,248,0.85)"},
                fillcolor="rgba(56,189,248,0.15)",
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin={"l": 40, "r": 10, "t": 40, "b": 40},
        height=240,
        xaxis={"title": "time (s)"},
        yaxis={"title": "spectral flatness", "range": [0, 1]},
    )
    return fig


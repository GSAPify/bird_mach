"""Tests for bird_mach.embedding feature extraction and UMAP."""

from __future__ import annotations

import numpy as np
import pytest

from bird_mach.embedding import (
    AudioFeatureConfig,
    UmapConfig,
    extract_log_mel_frames,
    stride_downsample,
)


class TestExtractLogMelFrames:
    def test_returns_correct_shapes(self, sine_wave: np.ndarray, sample_rate: int):
        cfg = AudioFeatureConfig(n_mels=64, hop_length=512)
        X, times, energy = extract_log_mel_frames(sine_wave, sr=sample_rate, cfg=cfg)
        assert X.ndim == 2
        assert X.shape[1] == 64
        assert times.shape[0] == X.shape[0]
        assert energy.shape[0] == X.shape[0]

    def test_dtype_is_float32(self, sine_wave: np.ndarray, sample_rate: int):
        cfg = AudioFeatureConfig()
        X, times, energy = extract_log_mel_frames(sine_wave, sr=sample_rate, cfg=cfg)
        assert X.dtype == np.float32
        assert times.dtype == np.float32
        assert energy.dtype == np.float32


class TestStrideDownsample:
    def test_stride_one_is_identity(self):
        X = np.ones((100, 10), dtype=np.float32)
        t = np.arange(100, dtype=np.float32)
        e = np.ones(100, dtype=np.float32)
        X2, t2, e2 = stride_downsample(X, t, e, stride=1)
        assert X2.shape[0] == 100

    def test_stride_reduces_length(self):
        X = np.ones((100, 10), dtype=np.float32)
        t = np.arange(100, dtype=np.float32)
        e = np.ones(100, dtype=np.float32)
        X2, t2, e2 = stride_downsample(X, t, e, stride=4)
        assert X2.shape[0] == 25


class TestUmapConfig:
    def test_defaults(self):
        cfg = UmapConfig()
        assert cfg.n_neighbors == 15
        assert cfg.min_dist == 0.1
        assert cfg.metric == "euclidean"

"""Tests for bird_mach.analysis pipeline functions."""

from __future__ import annotations

import numpy as np

from bird_mach.analysis import (
    OnsetResult,
    BeatResult,
    detect_onsets,
    track_beats,
    compute_zero_crossing_rate,
    compute_spectral_bandwidth,
)


class TestOnsetDetection:
    def test_returns_onset_result(self, sine_wave: np.ndarray, sample_rate: int):
        result = detect_onsets(sine_wave, sr=sample_rate)
        assert isinstance(result, OnsetResult)
        assert result.count >= 0
        assert len(result.times_s) == result.count

    def test_silence_has_few_onsets(self, silence: np.ndarray, sample_rate: int):
        result = detect_onsets(silence, sr=sample_rate)
        assert result.count <= 1


class TestBeatTracking:
    def test_returns_beat_result(self, sine_wave: np.ndarray, sample_rate: int):
        result = track_beats(sine_wave, sr=sample_rate)
        assert isinstance(result, BeatResult)
        assert result.tempo_bpm > 0

    def test_beat_times_are_sorted(self, sine_wave: np.ndarray, sample_rate: int):
        result = track_beats(sine_wave, sr=sample_rate)
        if result.beat_count > 1:
            assert np.all(np.diff(result.beat_times_s) >= 0)


class TestZeroCrossingRate:
    def test_shape_matches_frames(self, sine_wave: np.ndarray):
        zcr = compute_zero_crossing_rate(sine_wave, hop_length=512)
        assert zcr.ndim == 1
        assert zcr.dtype == np.float32

    def test_silence_has_zero_zcr(self, silence: np.ndarray):
        zcr = compute_zero_crossing_rate(silence)
        assert np.allclose(zcr, 0.0)


class TestSpectralBandwidth:
    def test_shape_and_dtype(self, sine_wave: np.ndarray, sample_rate: int):
        bw = compute_spectral_bandwidth(sine_wave, sr=sample_rate)
        assert bw.ndim == 1
        assert bw.dtype == np.float32

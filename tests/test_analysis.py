"""Tests for bird_mach.analysis pipeline functions."""

from __future__ import annotations

import numpy as np

from bird_mach.analysis import (
    OnsetResult,
    BeatResult,
    AnalysisSummary,
    detect_onsets,
    track_beats,
    compute_rms_energy,
    compute_zero_crossing_rate,
    compute_spectral_bandwidth,
    compute_spectral_rolloff,
    summarize,
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


class TestSummarize:
    def test_empty_input_returns_zero_summary(self):
        # Previously raised ValueError from librosa when given an empty array.
        empty = np.array([], dtype=np.float32)
        result = summarize(empty, sr=22050)
        assert isinstance(result, AnalysisSummary)
        assert result.duration_s == 0.0
        assert result.rms_mean == 0.0
        assert result.onset_count == 0
        assert result.tags == []


class TestSingleFrameOutputIsAlways1D:
    """Verify that sub-hop-length inputs yield 1-D arrays, not 0-D scalars.

    librosa feature functions return shape (1, 1) for very short signals;
    .squeeze() on that gives a 0-D array which breaks any ndim==1 assumption.
    """

    SHORT = np.ones(256, dtype=np.float32) * 0.1  # fewer samples than hop_length=512

    def test_rms_is_1d(self):
        result = compute_rms_energy(self.SHORT, hop_length=512)
        assert result.ndim == 1

    def test_zcr_is_1d(self):
        result = compute_zero_crossing_rate(self.SHORT, hop_length=512)
        assert result.ndim == 1

    def test_spectral_bandwidth_is_1d(self):
        result = compute_spectral_bandwidth(self.SHORT, sr=22050, hop_length=512)
        assert result.ndim == 1

    def test_spectral_rolloff_is_1d(self):
        result = compute_spectral_rolloff(self.SHORT, sr=22050, hop_length=512)
        assert result.ndim == 1

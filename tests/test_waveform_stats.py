"""Tests for bird_mach.waveform_stats."""

import numpy as np

from bird_mach.waveform_stats import compute_waveform_stats, WaveformStats


class TestWaveformStats:
    def test_returns_correct_type(self, sine_wave, sample_rate):
        stats = compute_waveform_stats(sine_wave, sr=sample_rate)
        assert isinstance(stats, WaveformStats)

    def test_peak_positive(self, sine_wave, sample_rate):
        stats = compute_waveform_stats(sine_wave, sr=sample_rate)
        assert stats.peak > 0

    def test_rms_less_than_peak(self, sine_wave, sample_rate):
        stats = compute_waveform_stats(sine_wave, sr=sample_rate)
        assert stats.rms <= stats.peak

    def test_silence_rms_zero(self, silence, sample_rate):
        stats = compute_waveform_stats(silence, sr=sample_rate)
        assert stats.rms == 0.0

    def test_duration_correct(self, sine_wave, sample_rate):
        stats = compute_waveform_stats(sine_wave, sr=sample_rate)
        assert abs(stats.duration_s - 1.0) < 0.01

    def test_n_samples(self, sine_wave, sample_rate):
        stats = compute_waveform_stats(sine_wave, sr=sample_rate)
        assert stats.n_samples == len(sine_wave)

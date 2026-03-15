"""Tests for built-in audio effects."""
import numpy as np
from bird_mach.plugin_system.builtin_effects import (
    GainEffect, LowPassFilter, HighPassFilter, CompressorEffect, ReverbEffect,
)

class TestGainEffect:
    def test_zero_db_passthrough(self):
        fx = GainEffect(db=0.0)
        x = np.ones(100, dtype=np.float32)
        assert np.allclose(fx.process(x, 44100), x)

class TestLowPassFilter:
    def test_reduces_high_freq(self):
        fx = LowPassFilter(cutoff_hz=100)
        t = np.linspace(0, 1, 44100, dtype=np.float32)
        x = np.sin(2 * np.pi * 10000 * t)
        result = fx.process(x, 44100)
        assert np.std(result) < np.std(x)

class TestCompressorEffect:
    def test_reduces_peaks(self):
        fx = CompressorEffect(threshold_db=-10, ratio=4)
        x = np.array([0.01, 0.5, 1.0, 0.8, 0.02], dtype=np.float32)
        result = fx.process(x, 44100)
        assert np.max(np.abs(result)) <= np.max(np.abs(x))

class TestReverbEffect:
    def test_adds_tail(self):
        fx = ReverbEffect(decay=0.5, delay_ms=10)
        x = np.zeros(4410, dtype=np.float32)
        x[0] = 1.0
        result = fx.process(x, 44100)
        assert np.any(result[440:] != 0)

"""Tests for bird_mach.effects."""

import numpy as np

from bird_mach.effects import apply_fade, mix


class TestApplyFade:
    def test_fade_in_starts_at_zero(self, sine_wave, sample_rate):
        result = apply_fade(sine_wave, sr=sample_rate, fade_in_s=0.1)
        assert abs(result[0]) < 1e-6

    def test_no_fade_is_identity(self, sine_wave, sample_rate):
        result = apply_fade(sine_wave, sr=sample_rate)
        assert np.allclose(result, sine_wave)

    def test_fade_out_ends_at_zero(self, sine_wave, sample_rate):
        result = apply_fade(sine_wave, sr=sample_rate, fade_out_s=0.1)
        assert abs(result[-1]) < 1e-6


class TestMix:
    def test_equal_mix(self):
        a = np.ones(100, dtype=np.float32)
        b = np.zeros(100, dtype=np.float32)
        result = mix(a, b, ratio=0.5)
        assert np.allclose(result, 0.5)

    def test_different_lengths(self):
        a = np.ones(100, dtype=np.float32)
        b = np.ones(50, dtype=np.float32)
        result = mix(a, b)
        assert len(result) == 50

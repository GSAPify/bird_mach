"""Tests for PhaseVocoder."""
import numpy as np

from bird_mach.realtime.phase_vocoder import PhaseVocoder


def test_high_rate_stretch_is_not_silent():
    y = np.random.default_rng(0).standard_normal(6144).astype(np.float32)
    out = PhaseVocoder().time_stretch(y, rate=10)
    assert np.any(out != 0)

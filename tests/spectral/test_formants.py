"""Tests for formant estimation."""
import numpy as np

from bird_mach.spectral.formants import estimate_formants


def vowel_like(sr=16000, n=4096):
    t = np.arange(n) / sr
    y = sum(np.sin(2 * np.pi * f * t) for f in (700, 1200, 2600))
    return y + 0.01 * np.random.default_rng(0).standard_normal(n)


def test_empty_input_returns_no_formants():
    assert estimate_formants(np.array([]), sr=16000) == []


def test_too_short_input_returns_no_formants():
    assert estimate_formants(np.ones(5), sr=16000) == []

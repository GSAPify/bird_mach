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


def test_silence_returns_no_formants():
    assert estimate_formants(np.zeros(2048), sr=16000) == []


def test_formants_are_sorted_and_in_range():
    sr = 16000
    formants = estimate_formants(vowel_like(sr), sr)
    assert formants
    assert formants == sorted(formants)
    assert all(90 < f < sr / 2 for f in formants)


def test_respects_n_formants():
    assert len(estimate_formants(vowel_like(), 16000, n_formants=2)) <= 2

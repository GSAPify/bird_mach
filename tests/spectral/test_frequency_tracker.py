"""Tests for FrequencyTracker."""
import numpy as np
import pytest

from bird_mach.spectral.frequency_tracker import FrequencyTracker

SR = 22050


def spectrum_with_peak(bin_index, n_bins=513):
    spec = np.zeros(n_bins)
    spec[bin_index] = 1.0
    return spec


def bin_freq(bin_index, n_bins=513):
    return bin_index * SR / (2 * (n_bins - 1))


def test_update_returns_peak_frequency():
    assert FrequencyTracker(sr=SR).update(spectrum_with_peak(100)) == pytest.approx(bin_freq(100))


def test_dc_bin_is_ignored():
    spec = spectrum_with_peak(5)
    spec[0] = 10.0
    assert FrequencyTracker(sr=SR).update(spec) == pytest.approx(bin_freq(5))


def test_short_spectrum_returns_zero_and_records_nothing():
    tracker = FrequencyTracker(sr=SR)
    assert tracker.update(np.array([1.0])) == 0.0
    assert tracker.current == 0.0


def test_current_is_zero_before_any_update():
    tracker = FrequencyTracker(sr=SR)
    assert tracker.current == 0.0
    assert tracker.smoothed == 0.0

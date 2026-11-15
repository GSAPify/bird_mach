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


def test_current_tracks_latest_update():
    tracker = FrequencyTracker(sr=SR)
    tracker.update(spectrum_with_peak(10))
    tracker.update(spectrum_with_peak(20))
    assert tracker.current == pytest.approx(bin_freq(20))


def test_smoothed_equals_current_with_few_samples():
    tracker = FrequencyTracker(sr=SR)
    tracker.update(spectrum_with_peak(10))
    tracker.update(spectrum_with_peak(30))
    assert tracker.smoothed == tracker.current


def test_smoothed_is_median_of_last_five():
    tracker = FrequencyTracker(sr=SR)
    for b in (10, 10, 500, 10, 10):
        tracker.update(spectrum_with_peak(b))
    assert tracker.smoothed == pytest.approx(bin_freq(10))


def test_trend_is_stable_with_short_history():
    tracker = FrequencyTracker(sr=SR)
    for b in range(10, 19):
        tracker.update(spectrum_with_peak(b * 10))
    assert tracker.trend == "stable"


def test_trend_rising():
    tracker = FrequencyTracker(sr=SR)
    for b in range(10, 110, 10):
        tracker.update(spectrum_with_peak(b))
    assert tracker.trend == "rising"


def test_trend_falling():
    tracker = FrequencyTracker(sr=SR)
    for b in range(100, 0, -10):
        tracker.update(spectrum_with_peak(b))
    assert tracker.trend == "falling"

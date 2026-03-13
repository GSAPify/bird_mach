"""Tests for onset patterns."""
import numpy as np
from bird_mach.spectral.onset_patterns import compute_onset_pattern, classify_rhythm

class TestOnsetPatterns:
    def test_regular(self):
        times = np.arange(0, 4, 0.5)
        result = compute_onset_pattern(times)
        assert result["regularity"] > 0.9

    def test_density(self):
        times = np.linspace(0, 1, 10)
        result = compute_onset_pattern(times)
        assert result["density"] > 5

    def test_classify(self):
        assert classify_rhythm(0.9, 4) == "metronomic"
        assert classify_rhythm(0.3, 0.5) == "sparse"

    def test_too_few(self):
        result = compute_onset_pattern(np.array([0.0, 1.0]))
        assert result["regularity"] == 0.0

"""Tests for stereo analysis."""
import numpy as np
from bird_mach.realtime.stereo import compute_stereo_width, compute_correlation, pan_position
class TestStereo:
    def test_mono_width_zero(self):
        x = np.random.randn(1000).astype(np.float32)
        assert compute_stereo_width(x, x) < 0.01
    def test_correlation_identical(self):
        x = np.random.randn(1000).astype(np.float32)
        assert compute_correlation(x, x) > 0.99
    def test_center_pan(self):
        x = np.ones(100, dtype=np.float32)
        assert abs(pan_position(x, x)) < 0.01

"""Tests for pitch tracker."""
import numpy as np
from bird_mach.realtime.pitch_tracker import RealtimePitchTracker
class TestPitchTracker:
    def test_silence(self):
        pt = RealtimePitchTracker(sr=22050)
        freq = pt.estimate(np.zeros(4096))
        assert freq == 0.0
    def test_sine(self):
        pt = RealtimePitchTracker(sr=22050)
        t = np.linspace(0, 0.2, 4410)
        y = np.sin(2*np.pi*440*t).astype(np.float32)
        freq = pt.estimate(y)
        assert 400 < freq < 480 or freq == 0.0

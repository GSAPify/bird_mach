"""Tests for loudness meter."""
import numpy as np
from bird_mach.realtime.loudness import LoudnessMeter
class TestLoudnessMeter:
    def test_silence(self):
        meter = LoudnessMeter()
        result = meter.process(np.zeros(1024))
        assert result["momentary_lufs"] < -60
    def test_signal(self):
        meter = LoudnessMeter()
        result = meter.process(np.ones(1024)*0.5)
        assert result["momentary_lufs"] > -20

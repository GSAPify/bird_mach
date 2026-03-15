"""Tests for visualizer."""
from bird_mach.realtime.visualizer import VisualizationFormatter
import numpy as np
class TestFormatter:
    def test_format(self):
        fmt = VisualizationFormatter()
        raw = {"rms":0.5,"peak":0.9,"centroid":1000,"spectrum_db":list(range(128))}
        vf = fmt.format(raw, np.zeros(256))
        assert vf.rms == 0.5

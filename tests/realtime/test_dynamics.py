"""Tests for DynamicsAnalyzer."""
import numpy as np
import pytest

from bird_mach.realtime.dynamics import DynamicsAnalyzer


def test_window_size_must_be_positive():
    with pytest.raises(ValueError):
        DynamicsAnalyzer(window_size=0)


def test_update_reports_peak_and_rms():
    stats = DynamicsAnalyzer(window_size=2).update(np.ones(4))
    assert stats["peak"] == 1.0
    assert stats["rms"] == pytest.approx(1.0)

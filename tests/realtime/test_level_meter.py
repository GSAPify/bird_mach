"""Tests for LevelMeter."""
import numpy as np
import pytest

from bird_mach.realtime.level_meter import PEAK_HOLD_DECAY_DB, LevelMeter


def test_peak_hold_decays_toward_quiet_signal():
    meter = LevelMeter()
    meter.read(np.full(64, 0.1))  # -20 dB
    for _ in range(200):
        reading = meter.read(np.full(64, 0.001))  # -60 dB
    assert reading.peak_db == pytest.approx(-20.0 - 200 * PEAK_HOLD_DECAY_DB, abs=1e-3)

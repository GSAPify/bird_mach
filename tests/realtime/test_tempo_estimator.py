"""Tests for TempoEstimator."""
import pytest

from bird_mach.realtime.tempo_estimator import TempoEstimator


def feed_pulses(est, frames, period):
    for i in range(frames):
        est.feed(1.0 if i % period == 0 else 0.0)


def test_rejects_invalid_sample_rate_and_hop():
    with pytest.raises(ValueError):
        TempoEstimator(sr=0)
    with pytest.raises(ValueError):
        TempoEstimator(hop=0)

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


def test_bpm_is_zero_until_enough_onsets():
    est = TempoEstimator()
    for _ in range(99):
        est.feed(1.0)
    assert est.bpm == 0.0


def test_detects_steady_pulse_train():
    est = TempoEstimator(sr=44100, hop=512)
    feed_pulses(est, 400, period=43)  # 43 frames at 512/44100 s is ~120 BPM
    assert est.bpm == pytest.approx(120.2, abs=1.5)


def test_tempo_survives_buffer_rollover():
    est = TempoEstimator(sr=44100, hop=512)
    feed_pulses(est, 1500, period=43)
    assert est.bpm == pytest.approx(120.2, abs=1.5)


def test_silence_has_no_tempo():
    est = TempoEstimator()
    for _ in range(200):
        est.feed(0.0)
    assert est.bpm == 0.0

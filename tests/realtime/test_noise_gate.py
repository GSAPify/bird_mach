"""Tests for NoiseGate."""
import numpy as np

from bird_mach.realtime.noise_gate import NoiseGate


def level(value, n=100):
    return np.full(n, value)


def test_gate_starts_closed():
    assert not NoiseGate().is_open


def test_loud_signal_opens_gate_and_passes_unchanged():
    gate = NoiseGate(threshold_db=-20.0)
    loud = level(0.5)
    out = gate.process(loud)
    assert gate.is_open
    assert np.array_equal(out, loud)

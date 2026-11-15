"""Tests for NoiseGate."""
import numpy as np

from bird_mach.realtime.noise_gate import NoiseGate


def level(value, n=100):
    return np.full(n, value)


def test_gate_starts_closed():
    assert not NoiseGate().is_open

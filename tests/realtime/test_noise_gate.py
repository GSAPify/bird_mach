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


def test_quiet_signal_is_attenuated():
    gate = NoiseGate(threshold_db=-20.0)
    quiet = level(0.01)
    assert np.allclose(gate.process(quiet), quiet * 0.01)
    assert not gate.is_open


def test_threshold_is_converted_from_db():
    gate = NoiseGate(threshold_db=-20.0)  # 0.1 linear
    gate.process(level(0.09))
    assert not gate.is_open
    gate.process(level(0.11))
    assert gate.is_open


def test_hysteresis_keeps_open_gate_open():
    gate = NoiseGate(threshold_db=-20.0)
    gate.process(level(0.5))
    gate.process(level(0.08))  # below threshold, above 70% of it
    assert gate.is_open


def test_gate_closes_when_signal_drops_well_below_threshold():
    gate = NoiseGate(threshold_db=-20.0)
    gate.process(level(0.5))
    gate.process(level(0.05))
    assert not gate.is_open

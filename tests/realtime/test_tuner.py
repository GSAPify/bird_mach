"""Tests for ChromaticTuner."""
import pytest

from bird_mach.realtime.tuner import ChromaticTuner

PLACEHOLDER = {"note": "—", "octave": 0, "cents": 0.0, "freq": 0.0}


def test_a440_is_a4():
    assert ChromaticTuner().tune(440.0) == {"note": "A", "octave": 4, "cents": 0.0, "freq": 440.0}


def test_middle_c():
    result = ChromaticTuner().tune(261.63)
    assert (result["note"], result["octave"]) == ("C", 4)
    assert abs(result["cents"]) < 1

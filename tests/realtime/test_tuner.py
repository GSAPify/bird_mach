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


def test_octave_up_is_a5():
    result = ChromaticTuner().tune(880.0)
    assert (result["note"], result["octave"]) == ("A", 5)


def test_lowest_piano_a():
    result = ChromaticTuner().tune(27.5)
    assert (result["note"], result["octave"]) == ("A", 0)


def test_sharp_note_name():
    result = ChromaticTuner().tune(466.16)
    assert (result["note"], result["octave"]) == ("A#", 4)


def test_sharp_pitch_reports_positive_cents():
    result = ChromaticTuner().tune(440.0 * 2 ** (25 / 1200))
    assert result["note"] == "A"
    assert result["cents"] == pytest.approx(25.0, abs=0.2)


def test_flat_pitch_reports_negative_cents():
    result = ChromaticTuner().tune(440.0 * 2 ** (-20 / 1200))
    assert result["note"] == "A"
    assert result["cents"] == pytest.approx(-20.0, abs=0.2)


def test_custom_reference_pitch():
    result = ChromaticTuner(a4_hz=432.0).tune(432.0)
    assert (result["note"], result["octave"]) == ("A", 4)
    assert result["cents"] == 0.0


def test_rejects_non_positive_reference():
    for bad in (0, -440.0):
        with pytest.raises(ValueError):
            ChromaticTuner(a4_hz=bad)

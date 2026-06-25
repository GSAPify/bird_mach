"""Tests for bird_mach.pitch."""

import numpy as np

from bird_mach.pitch import hz_to_note, estimate_pitch, PitchResult


class TestHzToNote:
    def test_a4(self):
        assert hz_to_note(440.0) == "A4"

    def test_c4(self):
        note = hz_to_note(261.63)
        assert note.startswith("C")

    def test_zero(self):
        assert hz_to_note(0.0) == "—"

    def test_negative(self):
        assert hz_to_note(-100.0) == "—"


class TestEstimatePitchEmpty:
    """The empty-input fast path in estimate_pitch was previously untested."""

    def test_returns_pitch_result(self):
        empty = np.array([], dtype=np.float32)
        result = estimate_pitch(empty, sr=22050)
        assert isinstance(result, PitchResult)

    def test_empty_arrays(self):
        empty = np.array([], dtype=np.float32)
        result = estimate_pitch(empty, sr=22050)
        assert result.f0.size == 0
        assert result.voiced_flag.size == 0
        assert result.times_s.size == 0

    def test_zero_scalars(self):
        empty = np.array([], dtype=np.float32)
        result = estimate_pitch(empty, sr=22050)
        assert result.median_hz == 0.0
        assert result.confidence == 0.0

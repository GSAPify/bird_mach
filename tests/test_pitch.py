"""Tests for bird_mach.pitch."""

from bird_mach.pitch import hz_to_note


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

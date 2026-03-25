"""Tests for screen reader descriptions."""
from bird_mach.accessibility.screen_reader import (
    describe_waveform, describe_spectrum, describe_tempo, describe_key,
)

class TestDescriptions:
    def test_waveform_loud(self):
        desc = describe_waveform(0.5, 0.8, 3.0)
        assert "loud" in desc

    def test_waveform_quiet(self):
        desc = describe_waveform(0.05, 0.1, 10.0)
        assert "quiet" in desc

    def test_spectrum(self):
        desc = describe_spectrum({"bass": 10, "mid": 5, "treble": 2})
        assert "bass" in desc

    def test_tempo(self):
        desc = describe_tempo(120)
        assert "120" in desc
        assert "upbeat" in desc

    def test_key(self):
        desc = describe_key("C", "major")
        assert "bright" in desc

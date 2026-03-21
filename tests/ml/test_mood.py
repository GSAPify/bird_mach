"""Tests for mood detection."""
from bird_mach.ml.mood_detector import detect_mood

class TestMoodDetector:
    def test_happy(self):
        moods = detect_mood(tempo=130, energy=0.2, mode="major")
        names = [m["mood"] for m in moods]
        assert "happy" in names

    def test_sad(self):
        moods = detect_mood(tempo=80, energy=0.08, mode="minor")
        names = [m["mood"] for m in moods]
        assert "sad" in names

    def test_energetic(self):
        moods = detect_mood(tempo=150, energy=0.4)
        assert any(m["mood"] == "energetic" for m in moods)

    def test_no_match(self):
        moods = detect_mood(tempo=105, energy=0.13)
        assert isinstance(moods, list)

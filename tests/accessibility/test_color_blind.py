"""Tests for color-blind palettes."""
from bird_mach.accessibility.color_blind import get_palette, get_high_contrast

class TestColorBlind:
    def test_default_palette(self):
        p = get_palette()
        assert len(p) == 6
        assert all(c.startswith("#") for c in p)

    def test_deuteranopia(self):
        p = get_palette("deuteranopia")
        assert len(p) == 6

    def test_unknown_falls_back(self):
        p = get_palette("nonexistent")
        assert p == get_palette("default")

    def test_high_contrast_dark(self):
        hc = get_high_contrast("dark")
        assert hc["background"] == "#000000"
        assert hc["text"] == "#FFFFFF"

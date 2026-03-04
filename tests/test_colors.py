"""Tests for bird_mach.visualization.colors."""

from bird_mach.visualization.colors import hex_to_rgba, interpolate_color, MACH_PALETTE


class TestHexToRgba:
    def test_white(self):
        assert hex_to_rgba("#ffffff") == "rgba(255,255,255,1.0)"

    def test_black_with_alpha(self):
        assert hex_to_rgba("#000000", 0.5) == "rgba(0,0,0,0.5)"

    def test_no_hash(self):
        assert hex_to_rgba("ff0000") == "rgba(255,0,0,1.0)"


class TestInterpolateColor:
    def test_start(self):
        assert interpolate_color((0, 0, 0), (255, 255, 255), 0.0) == (0, 0, 0)

    def test_end(self):
        assert interpolate_color((0, 0, 0), (255, 255, 255), 1.0) == (255, 255, 255)

    def test_midpoint(self):
        r, g, b = interpolate_color((0, 0, 0), (200, 100, 50), 0.5)
        assert r == 100
        assert g == 50


class TestPalette:
    def test_has_required_keys(self):
        assert "primary" in MACH_PALETTE
        assert "bg_dark" in MACH_PALETTE
        assert "error" in MACH_PALETTE

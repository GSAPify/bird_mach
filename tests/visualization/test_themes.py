"""Tests for Plotly layout themes."""
from bird_mach.visualization.colors import MACH_PALETTE
from bird_mach.visualization.themes import dark_layout, light_layout


def test_dark_layout_uses_palette_background():
    layout = dark_layout()
    assert layout["plot_bgcolor"] == MACH_PALETTE["bg_dark"]
    assert layout["paper_bgcolor"] == MACH_PALETTE["bg_dark"]


def test_dark_layout_uses_palette_text_color():
    assert dark_layout()["font"]["color"] == MACH_PALETTE["text"]


def test_dark_layout_override_replaces_key_only():
    layout = dark_layout(margin={"l": 0})
    assert layout["margin"] == {"l": 0}
    assert layout["font"]["color"] == MACH_PALETTE["text"]


def test_dark_layout_accepts_new_keys():
    assert dark_layout(title="Spectrum")["title"] == "Spectrum"


def test_light_layout_colors():
    layout = light_layout()
    assert layout["plot_bgcolor"] == "#ffffff"
    assert layout["paper_bgcolor"] == "#f8fafc"

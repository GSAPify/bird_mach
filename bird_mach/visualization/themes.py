"""Plotly layout themes for consistent visual styling."""

from __future__ import annotations

from bird_mach.visualization.colors import MACH_PALETTE


def dark_layout(**overrides) -> dict:
    """Return a Plotly layout dict for the Mach dark theme."""
    base = {
        "plot_bgcolor": MACH_PALETTE["bg_dark"],
        "paper_bgcolor": MACH_PALETTE["bg_dark"],
        "font": {"color": MACH_PALETTE["text"], "family": "system-ui, sans-serif"},
        "margin": {"l": 40, "r": 10, "t": 40, "b": 40},
        "coloraxis": {"colorbar": {"outlinewidth": 0}},
    }
    base.update(overrides)
    return base


def light_layout(**overrides) -> dict:
    """Return a Plotly layout dict for a light theme."""
    base = {
        "plot_bgcolor": "#ffffff",
        "paper_bgcolor": "#f8fafc",
        "font": {"color": "#1e293b", "family": "system-ui, sans-serif"},
        "margin": {"l": 40, "r": 10, "t": 40, "b": 40},
    }
    base.update(overrides)
    return base

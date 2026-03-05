"""Color utilities for Mach visualizations."""

from __future__ import annotations


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert #RRGGBB to rgba(r, g, b, a)."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def interpolate_color(
    c1: tuple[int, int, int],
    c2: tuple[int, int, int],
    t: float,
) -> tuple[int, int, int]:
    """Linearly interpolate between two RGB colors. t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


MACH_PALETTE = {
    "primary": "#38bdf8",
    "secondary": "#818cf8",
    "accent": "#fb923c",
    "success": "#4ade80",
    "error": "#f87171",
    "bg_dark": "#0f172a",
    "bg_card": "#1e293b",
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
}

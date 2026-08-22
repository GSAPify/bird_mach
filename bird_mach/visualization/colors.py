"""Color utilities for Mach visualizations."""

from __future__ import annotations


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert #RGB or #RRGGBB to rgba(r, g, b, a)."""
    value = hex_color.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6:
        raise ValueError(f"expected a 3- or 6-digit hex color, got {hex_color!r}")
    try:
        r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise ValueError(f"invalid hex color: {hex_color!r}") from exc
    alpha = max(0.0, min(1.0, alpha))
    return f"rgba({r},{g},{b},{alpha})"


def interpolate_color(
    c1: tuple[int, int, int],
    c2: tuple[int, int, int],
    t: float,
) -> tuple[int, int, int]:
    """Linearly interpolate between two RGB colors. t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    return (
        max(0, min(255, int(c1[0] + (c2[0] - c1[0]) * t))),
        max(0, min(255, int(c1[1] + (c2[1] - c1[1]) * t))),
        max(0, min(255, int(c1[2] + (c2[2] - c1[2]) * t))),
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

"""Color-blind friendly palette generation."""
from __future__ import annotations

PALETTES = {
    "default": ["#38bdf8", "#818cf8", "#f472b6", "#fb923c", "#4ade80", "#facc15"],
    "deuteranopia": ["#0072B2", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#CC79A7"],
    "protanopia": ["#0072B2", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#CC79A7"],
    "tritanopia": ["#332288", "#88CCEE", "#44AA99", "#117733", "#999933", "#CC6677"],
    "monochrome": ["#000000", "#333333", "#666666", "#999999", "#CCCCCC", "#FFFFFF"],
}

def get_palette(mode: str = "default") -> list[str]:
    return PALETTES.get(mode, PALETTES["default"])

def get_high_contrast(bg: str = "dark") -> dict[str, str]:
    if bg == "dark":
        return {"background": "#000000", "text": "#FFFFFF", "accent": "#FFFF00", "error": "#FF6B6B"}
    return {"background": "#FFFFFF", "text": "#000000", "accent": "#0000FF", "error": "#CC0000"}

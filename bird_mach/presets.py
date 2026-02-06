"""Visualization presets for common audio analysis scenarios."""

from __future__ import annotations

from dataclasses import dataclass

from bird_mach.embedding import AudioFeatureConfig, UmapConfig


@dataclass(frozen=True)
class VisualizationPreset:
    """Bundled configuration for a specific analysis scenario."""

    name: str
    description: str
    audio_config: AudioFeatureConfig
    umap_config: UmapConfig
    colorscale: str
    color_by: str
    stride: int


PRESET_MUSIC = VisualizationPreset(
    name="Music",
    description="Optimized for songs and musical recordings",
    audio_config=AudioFeatureConfig(n_mels=128, hop_length=512, fmin=20.0),
    umap_config=UmapConfig(n_neighbors=30, min_dist=0.05),
    colorscale="Turbo",
    color_by="time",
    stride=2,
)

PRESET_SPEECH = VisualizationPreset(
    name="Speech",
    description="Optimized for spoken word and podcasts",
    audio_config=AudioFeatureConfig(n_mels=64, hop_length=256, fmin=80.0),
    umap_config=UmapConfig(n_neighbors=20, min_dist=0.1),
    colorscale="Viridis",
    color_by="energy",
    stride=3,
)

PRESET_NATURE = VisualizationPreset(
    name="Nature / Field Recording",
    description="Optimized for environmental and nature sounds",
    audio_config=AudioFeatureConfig(n_mels=128, hop_length=1024, fmin=20.0),
    umap_config=UmapConfig(n_neighbors=15, min_dist=0.2),
    colorscale="Plasma",
    color_by="time",
    stride=1,
)

PRESET_PERCUSSIVE = VisualizationPreset(
    name="Percussive / Drums",
    description="Optimized for rhythmic and percussive content",
    audio_config=AudioFeatureConfig(n_mels=64, hop_length=256, fmin=20.0),
    umap_config=UmapConfig(n_neighbors=10, min_dist=0.01),
    colorscale="Hot",
    color_by="energy",
    stride=2,
)

ALL_PRESETS: dict[str, VisualizationPreset] = {
    "music": PRESET_MUSIC,
    "speech": PRESET_SPEECH,
    "nature": PRESET_NATURE,
    "percussive": PRESET_PERCUSSIVE,
}


def get_preset(name: str) -> VisualizationPreset | None:
    """Look up a preset by name (case-insensitive)."""
    return ALL_PRESETS.get(name.lower())

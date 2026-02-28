"""Tests for bird_mach.presets."""

from __future__ import annotations

from bird_mach.presets import (
    ALL_PRESETS,
    PRESET_MUSIC,
    PRESET_SPEECH,
    get_preset,
    VisualizationPreset,
)


class TestPresets:
    def test_all_presets_has_expected_keys(self):
        assert "music" in ALL_PRESETS
        assert "speech" in ALL_PRESETS
        assert "nature" in ALL_PRESETS
        assert "percussive" in ALL_PRESETS

    def test_preset_is_frozen(self):
        assert isinstance(PRESET_MUSIC, VisualizationPreset)
        assert isinstance(PRESET_SPEECH, VisualizationPreset)

    def test_get_preset_case_insensitive(self):
        assert get_preset("Music") is PRESET_MUSIC
        assert get_preset("SPEECH") is PRESET_SPEECH

    def test_get_preset_returns_none_for_unknown(self):
        assert get_preset("nonexistent") is None

    def test_presets_have_valid_colorscales(self):
        from bird_mach.constants import SUPPORTED_COLORSCALES
        for preset in ALL_PRESETS.values():
            assert preset.colorscale in SUPPORTED_COLORSCALES

    def test_presets_have_positive_stride(self):
        for preset in ALL_PRESETS.values():
            assert preset.stride >= 1

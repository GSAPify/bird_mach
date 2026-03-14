"""Tests for preset effect chains."""
import numpy as np
from bird_mach.plugin_system.preset_effects import PRESET_CHAINS
class TestPresetChains:
    def test_all_presets_exist(self):
        assert "vocal" in PRESET_CHAINS
        assert "master" in PRESET_CHAINS
        assert "ambient" in PRESET_CHAINS
    def test_vocal_chain_runs(self):
        chain = PRESET_CHAINS["vocal"]()
        x = np.random.randn(4410).astype(np.float32) * 0.5
        result = chain.process(x, 44100)
        assert len(result) == len(x)

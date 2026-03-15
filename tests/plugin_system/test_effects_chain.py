"""Tests for effects chain."""
import numpy as np
from bird_mach.plugin_system.effects_chain import EffectsChain
from bird_mach.plugin_system.builtin_effects import GainEffect, LowPassFilter

class TestEffectsChain:
    def test_empty_chain_passthrough(self):
        chain = EffectsChain()
        x = np.ones(100, dtype=np.float32)
        result = chain.process(x, 44100)
        assert np.allclose(result, x)

    def test_gain_effect(self):
        chain = EffectsChain()
        chain.add(GainEffect(db=6.0))
        x = np.ones(100, dtype=np.float32) * 0.5
        result = chain.process(x, 44100)
        assert np.all(result > x)

    def test_toggle(self):
        chain = EffectsChain()
        idx = chain.add(GainEffect(db=20.0))
        chain.toggle(idx)
        x = np.ones(100, dtype=np.float32)
        result = chain.process(x, 44100)
        assert np.allclose(result, x)

    def test_chain_info(self):
        chain = EffectsChain()
        chain.add(GainEffect(db=3.0))
        chain.add(LowPassFilter(cutoff_hz=1000))
        info = chain.get_chain_info()
        assert len(info) == 2
        assert info[0]["name"] == "gain"

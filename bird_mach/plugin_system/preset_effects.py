"""Pre-configured effect chain presets."""
from bird_mach.plugin_system.effects_chain import EffectsChain
from bird_mach.plugin_system.builtin_effects import *

def vocal_chain() -> EffectsChain:
    chain = EffectsChain()
    chain.add(HighPassFilter(cutoff_hz=80))
    chain.add(CompressorEffect(threshold_db=-15, ratio=3))
    chain.add(GainEffect(db=2.0))
    return chain

def master_chain() -> EffectsChain:
    chain = EffectsChain()
    chain.add(LowPassFilter(cutoff_hz=18000))
    chain.add(CompressorEffect(threshold_db=-10, ratio=2))
    chain.add(GainEffect(db=1.0))
    return chain

def ambient_chain() -> EffectsChain:
    chain = EffectsChain()
    chain.add(LowPassFilter(cutoff_hz=8000))
    chain.add(ReverbEffect(decay=0.5, delay_ms=80))
    return chain

PRESET_CHAINS = {"vocal": vocal_chain, "master": master_chain, "ambient": ambient_chain}

# Plugin System

## Architecture
Mach uses a registry-based plugin system with lifecycle hooks.

## Built-in Effects
- **Gain**: Volume adjustment in dB
- **Low Pass Filter**: Attenuate high frequencies
- **High Pass Filter**: Attenuate low frequencies
- **Compressor**: Dynamic range compression
- **Reverb**: Simple delay-based reverb

## Effects Chain
Chain multiple effects with per-effect wet/dry mixing.

```python
from bird_mach.plugin_system.effects_chain import EffectsChain
from bird_mach.plugin_system.builtin_effects import GainEffect, ReverbEffect

chain = EffectsChain()
chain.add(GainEffect(db=3.0))
chain.add(ReverbEffect(decay=0.3), wet_mix=0.4)
output = chain.process(samples, sr=44100)
```

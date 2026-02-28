# Visualization Presets

Mach ships with built-in presets optimized for different audio content types.

## Available Presets

### Music
Best for songs, instrumentals, and musical recordings.
- High mel-band resolution (128 bands)
- Moderate UMAP neighbors (30) for smooth clusters
- Turbo colorscale for vivid time progression

### Speech
Optimized for spoken word, podcasts, and voice recordings.
- Lower mel resolution (64 bands) focused on voice range
- Smaller hop length (256) for finer temporal detail
- Energy-based coloring to highlight volume dynamics

### Nature / Field Recording
Designed for environmental sounds, bird calls, and ambient recordings.
- Full frequency range with wide hop (1024)
- Higher min_dist for spread-out clusters
- Plasma colorscale for subtle gradients

### Percussive / Drums
Tuned for rhythmic content with sharp transients.
- Small hop length for precise onset capture
- Tight UMAP clustering (min_dist = 0.01)
- Hot colorscale emphasizing energy peaks

## Using Presets

```python
from bird_mach.presets import get_preset

preset = get_preset("music")
# Use preset.audio_config and preset.umap_config
```

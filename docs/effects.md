# Audio Effects

Mach includes a lightweight effects module for basic audio transformations.

## Available Effects

### Time Stretch
Change playback speed without affecting pitch.

```python
from bird_mach.effects import change_speed
fast = change_speed(y, rate=1.5)  # 50% faster
```

### Pitch Shift
Shift pitch by semitones without changing tempo.

```python
from bird_mach.effects import change_pitch
higher = change_pitch(y, sr=22050, n_steps=2)  # up 2 semitones
```

### Fade In/Out
Apply linear amplitude fades.

```python
from bird_mach.effects import apply_fade
y = apply_fade(y, sr=22050, fade_in_s=0.5, fade_out_s=1.0)
```

### Mix
Blend two audio signals.

```python
from bird_mach.effects import mix
blended = mix(vocal, instrumental, ratio=0.7)
```

# Accessibility

## Screen Reader Support
All visualizations generate text descriptions for screen readers.

```python
from bird_mach.accessibility.screen_reader import describe_waveform
desc = describe_waveform(rms=0.3, peak=0.8, duration_s=5.0)
```

## Color-Blind Friendly Palettes
Switch between palettes optimized for different types of color vision:
- Default, Deuteranopia, Protanopia, Tritanopia, Monochrome

## Keyboard Shortcuts
Full keyboard navigation with customizable shortcuts.
Press `?` to show the shortcut help panel.

## High Contrast Mode
Dark and light high-contrast themes available.

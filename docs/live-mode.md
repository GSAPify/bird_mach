# Live Mode Guide

## Overview

Live mode provides real-time audio visualization directly in the browser using the Web Audio API. No server-side processing is required — everything runs client-side.

## Audio Sources

| Source | Description | How to activate |
|--------|-------------|-----------------|
| **File** | Load a local audio file | Drag & drop or click browse |
| **Microphone** | Capture from mic | Click the mic button |
| **Screen/Tab** | Capture system or tab audio | Click the screen button |

## Visualizations

### Waveform
Real-time oscilloscope view showing the raw audio signal amplitude.

### Spectrogram
Rolling frequency-domain view using FFT, displayed as a color-mapped waterfall.

### Frequency Bands
Three-bar display showing energy in bass (20-300 Hz), mid (300-4000 Hz), and treble (4000+ Hz) ranges.

### 3D Point Cloud
Interactive Three.js scatter plot that maps audio features to 3D coordinates in real time.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `C` | Clear canvases |
| `M` | Toggle microphone |
| `F` | Toggle fullscreen on 3D cloud |

## Stats Panel

The real-time stats overlay shows:
- **RMS**: Root mean square energy level
- **Peak**: Maximum amplitude in current buffer
- **Centroid**: Spectral centroid (brightness indicator)
- **Time**: Elapsed playback time

# Live Mode Guide

## Overview

Live mode provides real-time audio visualization directly in the browser using the Web Audio API. No server-side processing is required — everything runs client-side.

## Audio Sources

| Source | Description | How to activate |
|--------|-------------|-----------------|
| **File** | Load a local audio file | Drag & drop or click browse |
| **Microphone** | Capture from a chosen local mic | Click **Check mic**, allow the browser prompt, then click **Mic** |
| **Screen/Tab** | Capture system or tab audio | Click the screen button |

## Local Microphone Permission

Browser microphone capture is allowed on HTTPS origins and on local secure
contexts such as `http://localhost:8000` and `http://127.0.0.1:8000`.

1. Start the app with `python -m bird_mach serve --host 127.0.0.1 --port 8000`.
2. Open `http://127.0.0.1:8000/live`.
3. Click **Check mic** and approve the browser microphone prompt.
4. Choose a microphone input if more than one device is listed.
5. Click **Mic** to start the live analyzer.

If the browser blocks the prompt, enable microphone access in the browser's
site settings for `127.0.0.1` or `localhost` and retry **Check mic**.

## Visualizations

### Waveform
Real-time oscilloscope view showing the raw audio signal amplitude.

### Spectrogram
Rolling frequency-domain view using FFT, displayed as a color-mapped waterfall.

### Frequency Bands
Seven-band display showing energy from sub/bass through air/edge ranges.

### 3D Point Cloud
Interactive Plotly scatter plot that maps audio features to 3D coordinates in real time.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `C` | Clear canvases |
| `M` | Start microphone capture |

## Stats Panel

The real-time stats overlay shows:
- **RMS**: Root mean square energy level
- **Peak**: Maximum amplitude in current buffer
- **Centroid**: Spectral centroid (brightness indicator)
- **Time**: Elapsed playback time

# Mach — 3D Audio Visualization

Visualize **any audio** — music, speech, bird calls, field recordings — as interactive 3D point clouds. Each point represents a short-time frame of the recording, embedded into 2D or 3D space via UMAP on log-mel spectrogram features.

## What it does

- **Input**: any audio file (WAV, MP3, FLAC, OGG, M4A) or a URL to one
- **Process**: compute a log-mel spectrogram, then embed per-frame vectors with UMAP
- **Output**: interactive Plotly visualizations (2D scatter or 3D multi-view point cloud)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI

Generate a standalone HTML visualization:

```bash
python scripts/bird_sound_3d.py --input recording.wav --output viz.html --multi-view --connect
```

Options: `--color-by time|energy`, `--stride N`, `--n-neighbors`, `--min-dist`

## Web app

```bash
uvicorn bird_mach.webapp:app --reload --port 8000
```

Open `http://127.0.0.1:8000` in your browser.

### Upload mode (`/`)

- **Drag & drop** or click to upload any audio file
- **Paste a URL** to a remote audio file
- Choose between **2D** or **3D** UMAP projections
- Pick from **8 colorscales** (Turbo, Viridis, Plasma, etc.)
- Toggle multi-view (3 camera angles) and point connections

### Live mode (`/live`)

Real-time audio visualization with **4 sources**:

| Source | Description |
|--------|-------------|
| **File** | Load a local audio file and play it |
| **Mic** | Capture from your microphone |
| **Tab audio** | Capture audio from another browser tab (Spotify, YouTube, etc.) |

Live mode includes:

- **Frequency band bars** — 7 color-coded bands (Sub through Air)
- **Waveform** — real-time amplitude display
- **Scrolling spectrogram** — frequency content over time
- **3D point cloud** — audio-reactive with loop or cloud motion
- **Live stats** — RMS energy, peak, spectral centroid, elapsed time
- **Fullscreen** — expand the 3D view to fill the screen
- **Keyboard shortcuts** — Space (play/stop), C (clear), M (mic)

## API endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Upload form with drag-drop, URL input, 2D/3D toggle |
| `/live` | GET | Real-time visualization (file, mic, or tab audio) |
| `/visualize` | POST | Process audio and return interactive plots |
| `/health` | GET | Health check (`{"status": "ok"}`) |

## Analysis CLI

Run a full-feature analysis on any audio file:

```bash
python scripts/analyze_audio.py recording.wav --output result.json
```

Batch-process a directory:

```bash
python scripts/batch_process.py ./samples/ --output results/
```

See [docs/api.md](docs/api.md) for the full Python API reference and [docs/presets.md](docs/presets.md) for built-in visualization presets.

## n8n Workflows

The `workflows/` directory contains automation workflows for n8n. See [`workflows/README.md`](workflows/README.md) for details.

## License

MIT. See `LICENSE`.

# Bird Mach — 3D Bird Sound Visualization (Prototype)

This repo contains a small prototype to create **3D “sound maps”** like the screenshot you shared: a point cloud/trajectory where each point represents a short-time slice of audio embedded into 3D (UMAP).

## What this visualization is

- **Input**: a `.wav` recording
- **Process**:
  - compute a log-mel spectrogram (one feature vector per time frame)
  - embed the per-frame feature vectors into 3D with UMAP
- **Output**: interactive Plotly HTML with stacked multi-view 3D plots

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Generate an interactive HTML:

```bash
python scripts/bird_sound_3d.py --input /path/to/audio.wav --output /path/to/out.html --multi-view --connect
```

## Local web app

Run the local server:

```bash
uvicorn bird_mach.webapp:app --reload --port 8000
```

Then open `http://127.0.0.1:8000` in your browser.

Routes:

- `/`: upload a clip and generate the UMAP 3D embedding + extra plots (waveform, spectrogram, energy)
- `/live`: real-time visuals while audio plays (waveform + scrolling spectrogram + 3D point cloud)

Notes:

- Live mode uses the browser’s WebAudio API. For microphone mode you’ll be prompted for mic permission.
- If live mode feels slow, lower `max points` or `bins`.

Common options:

- `--color-by time|energy` (default: `time`)
- `--stride N` (downsample frames; useful for long recordings)

## API endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Upload form for batch UMAP visualization |
| `/live` | GET | Real-time audio visualization (mic or file) |
| `/visualize` | POST | Process uploaded audio and return results |
| `/health` | GET | Health check (returns `{"status": "ok"}`) |

## Notes

- Works best with relatively clean clips (a few seconds to a couple minutes).
- For very long recordings, increase `--stride` to keep the plot responsive.
- The `/health` endpoint can be used by load balancers and uptime monitors.

## n8n Workflows

The `workflows/` directory contains automation workflows for n8n. See [`workflows/README.md`](workflows/README.md) for details.

## License

MIT. See `LICENSE`.

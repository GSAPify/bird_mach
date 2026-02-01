# API Reference

## Endpoints

### `GET /`
Upload form for audio file analysis.

**Response**: HTML page with drag-and-drop upload form.

### `POST /visualize`
Process uploaded audio and return interactive visualizations.

**Form Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file` | UploadFile | - | Audio file (wav, mp3, flac, etc.) |
| `audio_url` | string | "" | URL to fetch audio from |
| `stride` | int | 2 | Downsample stride (1-20) |
| `n_neighbors` | int | 15 | UMAP neighbor count (5-200) |
| `min_dist` | float | 0.1 | UMAP min distance (0.0-1.0) |
| `color_by` | string | "time" | Color mode: "time" or "energy" |
| `view` | string | "single" | View: "single" or "multi" |
| `colorscale` | string | "Turbo" | Plotly colorscale name |
| `dimensions` | string | "3d" | Projection: "2d" or "3d" |

**Response**: HTML page with Plotly figures.

### `GET /live`
Real-time browser-based audio visualization.

**Response**: HTML page with Web Audio API visualizations.

### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "ok",
  "app": "Mach",
  "version": "0.3.0"
}
```

## Python API

### `bird_mach.embedding`

```python
from bird_mach.embedding import (
    AudioFeatureConfig,
    UmapConfig,
    load_audio_mono_from_path,
    extract_log_mel_frames,
    compute_umap_3d,
    build_singleview_figure,
)
```

### `bird_mach.analysis`

```python
from bird_mach.analysis import (
    detect_onsets,
    track_beats,
    summarize,
)
```

### `bird_mach.exporters`

```python
from bird_mach.exporters import to_json, features_to_csv
```

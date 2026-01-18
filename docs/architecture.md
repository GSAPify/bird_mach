# Architecture

## Overview

Mach is a Python-based audio visualization application built on FastAPI. It processes audio through a pipeline of feature extraction, dimensionality reduction, and interactive visualization.

## Module Structure

```
bird_mach/
├── __init__.py          # Package exports
├── analysis.py          # High-level analysis pipeline
├── constants.py         # Shared configuration constants
├── embedding.py         # Feature extraction + UMAP + Plotly
├── exceptions.py        # Custom exception hierarchy
├── exporters.py         # JSON/CSV output
├── types.py             # Type aliases
└── webapp.py            # FastAPI routes and HTML templates
```

## Data Flow

```
Audio Input
    │
    ▼
┌──────────────┐
│  Load & Mono │  librosa.load()
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Log-Mel     │  extract_log_mel_frames()
│  Spectrogram │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Downsample  │  stride_downsample()
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  UMAP        │  compute_umap_3d() / compute_umap_2d()
│  Projection  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Plotly       │  build_*_figure()
│  Visualization│
└──────────────┘
```

## Key Design Decisions

1. **Stateless Processing**: Each request processes audio from scratch — no server-side session state.
2. **Config Dataclasses**: `AudioFeatureConfig` and `UmapConfig` use frozen dataclasses for immutability.
3. **Template Inlining**: HTML templates are embedded in `webapp.py` to keep the project self-contained.
4. **Dual Mode**: Upload mode for file analysis, Live mode for real-time browser-based visualization.

# Mach — Audio Intelligence Platform

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]
[![Python](https://img.shields.io/badge/python-3.11+-blue)]
[![License](https://img.shields.io/badge/license-MIT-green)]

**Mach** is an enterprise-grade audio analysis and visualization platform.

## Features

- **Real-time Engine** — Low-latency audio processing with WebSocket streaming
- **Audio Fingerprinting** — Chromaprint and constellation-based matching
- **Collaboration** — Rooms, annotations, comments, presence, sharing
- **Plugin System** — Extensible effects chain with built-in DSP
- **Analysis** — Spectral, temporal, harmonic analysis with UMAP visualization
- **Reporting** — Markdown, HTML, CSV, JSONL export with scheduled reports
- **Dashboard** — Usage analytics, alerts, leaderboard
- **API** — RESTful API v1 with Pydantic validation

## Quick Start

```bash
pip install -r requirements.txt
python -m bird_mach serve
```

## CLI

```bash
python -m bird_mach analyze audio.wav
python -m bird_mach compare a.wav b.wav
python -m bird_mach version
```

## Docker

```bash
docker compose up
```

## Documentation

See [docs/](docs/) for guides on:
- [Architecture](docs/architecture.md)
- [API Reference](docs/api-v1.md)
- [Real-time Engine](docs/enterprise/realtime.md)
- [Fingerprinting](docs/enterprise/fingerprinting.md)
- [Collaboration](docs/enterprise/collaboration.md)
- [Plugin System](docs/enterprise/plugins.md)
- [Dashboard](docs/enterprise/dashboard.md)
- [Reporting](docs/enterprise/reporting.md)
- [Deployment](docs/deployment.md)

## License

MIT

# Changelog

All notable changes to Mach are documented here.

## [0.2.0] - 2026-02-21

### Added
- Universal audio visualization — any sound, any source (not just bird calls).
- Live mode with microphone, file, and screen/tab capture.
- Frequency band bars (bass / mid / treble) in live view.
- Real-time audio stats overlay (RMS, peak, centroid).
- Drag-and-drop file upload.
- URL-based audio loading.
- 2D / 3D dimension toggle for UMAP embeddings.
- Multiple colorscale options (Turbo, Viridis, Plasma, etc.).
- Spectral flatness computation and chart.
- Custom exception hierarchy for structured error handling.
- Audio utilities module (probe, normalize, silence trim).
- Type aliases for numpy arrays.
- Keyboard shortcuts in live mode (Space, C, M).
- Fullscreen toggle for 3D point cloud.
- `/health` endpoint for uptime monitoring.
- CORS middleware.

### Changed
- Rebranded from "Bird Mach" to "Mach".
- Lowered default `fmin` from 150 Hz to 20 Hz for general audio.
- Added upper-bound version pins to requirements.txt.

### Fixed
- Feature matrix shape validation before UMAP projection.
- Safe parameter clamping on user-supplied values.

## [0.1.0] - 2026-01-07

### Added
- Initial 3D bird sound visualization with UMAP embeddings.
- Log-mel spectrogram feature extraction.
- Multi-view and single-view 3D Plotly figures.
- Waveform and spectrogram charts.
- FastAPI web application with upload form.
- CLI script for batch processing.

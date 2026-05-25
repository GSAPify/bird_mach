# Source Module Index

This index maps notable runtime modules to their purpose so contributors can find implementation areas quickly.

| Module | Purpose |
|--------|---------|
| [`bird_mach/__main__.py`](../bird_mach/__main__.py) | Allow running Mach as: python -m bird_mach |
| [`bird_mach/accessibility/color_blind.py`](../bird_mach/accessibility/color_blind.py) | Color-blind friendly palette generation |
| [`bird_mach/accessibility/keyboard_shortcuts.py`](../bird_mach/accessibility/keyboard_shortcuts.py) | Keyboard shortcut registry and documentation |
| [`bird_mach/accessibility/screen_reader.py`](../bird_mach/accessibility/screen_reader.py) | Screen reader friendly descriptions for visualizations |
| [`bird_mach/analysis.py`](../bird_mach/analysis.py) | High-level audio analysis pipeline for Mach |
| [`bird_mach/api/responses.py`](../bird_mach/api/responses.py) | Standardized API response helpers |
| [`bird_mach/api/routes.py`](../bird_mach/api/routes.py) | API v1 routes for programmatic access to Mach analysis |
| [`bird_mach/api/schemas.py`](../bird_mach/api/schemas.py) | Pydantic schemas for the Mach REST API |
| [`bird_mach/api/v2/filters.py`](../bird_mach/api/v2/filters.py) | Query filter parsing and application for API v2 |
| [`bird_mach/api/v2/pagination.py`](../bird_mach/api/v2/pagination.py) | Cursor-based and offset pagination utilities |
| [`bird_mach/api/v2/rate_limit.py`](../bird_mach/api/v2/rate_limit.py) | API v2 rate limiting middleware |
| [`bird_mach/api/v2/versioning.py`](../bird_mach/api/v2/versioning.py) | Reference for api v2 versioning |
| [`bird_mach/audio_formats/converter.py`](../bird_mach/audio_formats/converter.py) | Audio format conversion utilities |
| [`bird_mach/audio_formats/detector.py`](../bird_mach/audio_formats/detector.py) | Detect audio format from file headers |
| [`bird_mach/audio_formats/metadata.py`](../bird_mach/audio_formats/metadata.py) | Audio file metadata extraction |
| [`bird_mach/audio_formats/normalize.py`](../bird_mach/audio_formats/normalize.py) | Audio normalization utilities |
| [`bird_mach/audio_utils.py`](../bird_mach/audio_utils.py) | Lightweight audio utility helpers — duration, format detection, normalization |
| [`bird_mach/batch/file_scanner.py`](../bird_mach/batch/file_scanner.py) | Scan directories for audio files |
| [`bird_mach/batch/pipeline.py`](../bird_mach/batch/pipeline.py) | Configurable batch processing pipeline |
| [`bird_mach/batch/progress.py`](../bird_mach/batch/progress.py) | Progress tracking for batch operations |
| [`bird_mach/batch/queue.py`](../bird_mach/batch/queue.py) | Job queue for background batch processing |
| [`bird_mach/batch/result_aggregator.py`](../bird_mach/batch/result_aggregator.py) | Aggregate results from batch processing runs |
| [`bird_mach/cache.py`](../bird_mach/cache.py) | Simple in-memory LRU cache for expensive audio computations |
| [`bird_mach/caching/cache_key.py`](../bird_mach/caching/cache_key.py) | Cache key generation utilities |
| [`bird_mach/caching/disk_cache.py`](../bird_mach/caching/disk_cache.py) | Disk-based cache for large analysis results |

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
| [`bird_mach/caching/memory_cache.py`](../bird_mach/caching/memory_cache.py) | In-memory LRU cache with TTL support |
| [`bird_mach/caching/strategy_v1.py`](../bird_mach/caching/strategy_v1.py) | Cache invalidation strategy variant 1 |
| [`bird_mach/caching/strategy_v2.py`](../bird_mach/caching/strategy_v2.py) | Cache invalidation strategy variant 2 |
| [`bird_mach/caching/strategy_v3.py`](../bird_mach/caching/strategy_v3.py) | Cache invalidation strategy variant 3 |
| [`bird_mach/caching/tiered_cache.py`](../bird_mach/caching/tiered_cache.py) | Two-tier cache combining memory and disk layers |
| [`bird_mach/caching/warming.py`](../bird_mach/caching/warming.py) | Cache warming strategies |
| [`bird_mach/cli/main.py`](../bird_mach/cli/main.py) | Unified CLI entry point for Mach audio tools |
| [`bird_mach/clustering.py`](../bird_mach/clustering.py) | Clustering wrappers for grouping audio frames or segments |
| [`bird_mach/collaboration/annotations.py`](../bird_mach/collaboration/annotations.py) | Time-stamped annotations for collaborative audio review |
| [`bird_mach/collaboration/comments.py`](../bird_mach/collaboration/comments.py) | Threaded comments for audio analysis discussions |
| [`bird_mach/collaboration/cursor_sync.py`](../bird_mach/collaboration/cursor_sync.py) | Cursor synchronization for collaborative audio review |
| [`bird_mach/collaboration/export_session.py`](../bird_mach/collaboration/export_session.py) | Export collaboration sessions for archival |
| [`bird_mach/collaboration/permissions.py`](../bird_mach/collaboration/permissions.py) | Fine-grained permissions for collaboration |
| [`bird_mach/collaboration/presence.py`](../bird_mach/collaboration/presence.py) | Real-time presence tracking for collaboration rooms |
| [`bird_mach/collaboration/rooms.py`](../bird_mach/collaboration/rooms.py) | Collaboration rooms for shared audio analysis sessions |
| [`bird_mach/collaboration/sharing.py`](../bird_mach/collaboration/sharing.py) | Audio sharing and link generation |
| [`bird_mach/collaboration/versioning.py`](../bird_mach/collaboration/versioning.py) | Version control for audio analysis configurations |
| [`bird_mach/compare.py`](../bird_mach/compare.py) | Compare two audio analysis summaries side by side |
| [`bird_mach/config.py`](../bird_mach/config.py) | Application configuration loaded from environment variables |
| [`bird_mach/constants.py`](../bird_mach/constants.py) | Application constants for Mach |
| [`bird_mach/dashboard/activity_feed.py`](../bird_mach/dashboard/activity_feed.py) | Activity feed for tracking user actions |
| [`bird_mach/dashboard/alerts.py`](../bird_mach/dashboard/alerts.py) | Alert rules and notification triggers |
| [`bird_mach/dashboard/leaderboard.py`](../bird_mach/dashboard/leaderboard.py) | Usage leaderboard for gamification |
| [`bird_mach/dashboard/stats.py`](../bird_mach/dashboard/stats.py) | Dashboard statistics aggregation |

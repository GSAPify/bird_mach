# Caching Architecture

## Layers
- **L1 (Memory)**: LRU cache with TTL, sub-millisecond access
- **L2 (Disk)**: JSON-based, survives restarts, larger capacity

## Tiered Cache
Reads check L1 first, then L2. L2 hits promote to L1.

```python
from bird_mach.caching.tiered_cache import TieredCache
cache = TieredCache(Path("/tmp/mach-cache"))
cache.set("analysis:abc", {"rms": 0.3, "tempo": 120})
result = cache.get("analysis:abc")
```

## Cache Keys
Deterministic key generation based on file content hash + parameters.

## Warming
Pre-populate cache on startup with frequently accessed analyses.

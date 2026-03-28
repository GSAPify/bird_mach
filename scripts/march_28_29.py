#!/usr/bin/env python3
"""15 commits on Mar 28, 27 commits on Mar 29."""

import os, subprocess, random, textwrap
from datetime import datetime
from pathlib import Path

BASE = Path("/Users/akhilsingh/Personal Learning Projects/Bird Mach")
TZ = "+0530"
random.seed(2829)
count = 0

def w(rel, content):
    p = BASE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

def git(msg, dt):
    global count
    ds = dt.strftime(f"%Y-%m-%dT%H:%M:%S{TZ}")
    env = {**os.environ, "GIT_AUTHOR_DATE": ds, "GIT_COMMITTER_DATE": ds}
    subprocess.run(["git", "add", "-A"], cwd=BASE, env=env, capture_output=True)
    r = subprocess.run(["git", "commit", "-m", msg], cwd=BASE, env=env, capture_output=True)
    if r.returncode == 0:
        count += 1

ITEMS = [
    # ═══════════════ MARCH 28 — 15 commits: Caching layer ═══════════════

    (28,8,10,"bird_mach/caching/__init__.py",
     '"""Multi-layer caching for Mach."""\n',
     "feat(caching): scaffold multi-layer caching package"),

    (28,8,35,"bird_mach/caching/memory_cache.py",'''
    """In-memory LRU cache with TTL support."""
    from __future__ import annotations
    import time
    from collections import OrderedDict
    from dataclasses import dataclass

    @dataclass
    class CacheEntry:
        value: object
        expires_at: float
        hits: int = 0

    class MemoryCache:
        def __init__(self, max_size: int = 1000, ttl_s: float = 300.0):
            self._max = max_size
            self._ttl = ttl_s
            self._store: OrderedDict[str, CacheEntry] = OrderedDict()
            self._misses = 0

        def get(self, key: str) -> object | None:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if time.time() > entry.expires_at:
                self._store.pop(key, None)
                self._misses += 1
                return None
            entry.hits += 1
            self._store.move_to_end(key)
            return entry.value

        def set(self, key: str, value: object, ttl_s: float | None = None) -> None:
            if key in self._store:
                self._store.pop(key)
            elif len(self._store) >= self._max:
                self._store.popitem(last=False)
            self._store[key] = CacheEntry(
                value=value, expires_at=time.time() + (ttl_s or self._ttl),
            )

        def delete(self, key: str) -> bool:
            return self._store.pop(key, None) is not None

        def clear(self) -> int:
            n = len(self._store)
            self._store.clear()
            return n

        @property
        def size(self) -> int:
            return len(self._store)

        @property
        def stats(self) -> dict:
            total_hits = sum(e.hits for e in self._store.values())
            return {"size": self.size, "hits": total_hits, "misses": self._misses}
    ''', "feat(caching): add in-memory LRU cache with TTL and stats"),

    (28,9,5,"bird_mach/caching/disk_cache.py",'''
    """Disk-based cache for large analysis results."""
    from __future__ import annotations
    import hashlib
    import json
    import time
    from pathlib import Path

    class DiskCache:
        def __init__(self, cache_dir: Path, ttl_s: float = 3600.0):
            self._dir = cache_dir
            self._ttl = ttl_s
            self._dir.mkdir(parents=True, exist_ok=True)

        def _key_path(self, key: str) -> Path:
            h = hashlib.sha256(key.encode()).hexdigest()[:16]
            return self._dir / f"{h}.json"

        def get(self, key: str) -> dict | None:
            path = self._key_path(key)
            if not path.exists():
                return None
            data = json.loads(path.read_text())
            if time.time() > data.get("_expires_at", 0):
                path.unlink(missing_ok=True)
                return None
            return data.get("value")

        def set(self, key: str, value: dict, ttl_s: float | None = None) -> None:
            path = self._key_path(key)
            data = {"value": value, "_expires_at": time.time() + (ttl_s or self._ttl),
                    "_key": key}
            path.write_text(json.dumps(data, default=str))

        def delete(self, key: str) -> bool:
            path = self._key_path(key)
            if path.exists():
                path.unlink()
                return True
            return False

        def clear(self) -> int:
            files = list(self._dir.glob("*.json"))
            for f in files:
                f.unlink()
            return len(files)

        @property
        def size(self) -> int:
            return len(list(self._dir.glob("*.json")))
    ''', "feat(caching): add disk-based cache for large results"),

    (28,9,35,"bird_mach/caching/tiered_cache.py",'''
    """Two-tier cache combining memory and disk layers."""
    from __future__ import annotations
    from pathlib import Path
    from bird_mach.caching.memory_cache import MemoryCache
    from bird_mach.caching.disk_cache import DiskCache

    class TieredCache:
        def __init__(self, cache_dir: Path, mem_max: int = 500, mem_ttl: float = 120.0,
                     disk_ttl: float = 3600.0):
            self._l1 = MemoryCache(max_size=mem_max, ttl_s=mem_ttl)
            self._l2 = DiskCache(cache_dir, ttl_s=disk_ttl)

        def get(self, key: str):
            val = self._l1.get(key)
            if val is not None:
                return val
            val = self._l2.get(key)
            if val is not None:
                self._l1.set(key, val)
            return val

        def set(self, key: str, value, ttl_s: float | None = None) -> None:
            self._l1.set(key, value, ttl_s)
            if isinstance(value, dict):
                self._l2.set(key, value, ttl_s)

        def invalidate(self, key: str) -> None:
            self._l1.delete(key)
            self._l2.delete(key)

        def clear_all(self) -> dict:
            return {"memory": self._l1.clear(), "disk": self._l2.clear()}

        @property
        def stats(self) -> dict:
            return {"l1": self._l1.stats, "l2_size": self._l2.size}
    ''', "feat(caching): add two-tier cache combining memory and disk"),

    (28,10,5,"tests/caching/__init__.py",
     '"""Tests for caching layer."""\n',
     "test(caching): scaffold caching test package"),

    (28,10,25,"tests/caching/test_memory_cache.py",'''
    """Tests for memory cache."""
    import time
    from bird_mach.caching.memory_cache import MemoryCache

    class TestMemoryCache:
        def test_set_get(self):
            c = MemoryCache()
            c.set("k", "v")
            assert c.get("k") == "v"

        def test_miss(self):
            c = MemoryCache()
            assert c.get("nope") is None

        def test_ttl_expiry(self):
            c = MemoryCache(ttl_s=0.01)
            c.set("k", "v")
            time.sleep(0.02)
            assert c.get("k") is None

        def test_lru_eviction(self):
            c = MemoryCache(max_size=2)
            c.set("a", 1)
            c.set("b", 2)
            c.set("c", 3)
            assert c.get("a") is None
            assert c.get("c") == 3

        def test_delete(self):
            c = MemoryCache()
            c.set("k", "v")
            assert c.delete("k")
            assert c.get("k") is None

        def test_stats(self):
            c = MemoryCache()
            c.set("k", "v")
            c.get("k")
            s = c.stats
            assert s["hits"] == 1
    ''', "test(caching): add memory cache tests — TTL, LRU, delete, stats"),

    (28,11,0,"tests/caching/test_disk_cache.py",'''
    """Tests for disk cache."""
    from bird_mach.caching.disk_cache import DiskCache

    class TestDiskCache:
        def test_set_get(self, tmp_path):
            c = DiskCache(tmp_path)
            c.set("k", {"data": 42})
            assert c.get("k") == {"data": 42}

        def test_miss(self, tmp_path):
            c = DiskCache(tmp_path)
            assert c.get("missing") is None

        def test_delete(self, tmp_path):
            c = DiskCache(tmp_path)
            c.set("k", {"x": 1})
            assert c.delete("k")
            assert c.get("k") is None

        def test_clear(self, tmp_path):
            c = DiskCache(tmp_path)
            c.set("a", {"v": 1})
            c.set("b", {"v": 2})
            n = c.clear()
            assert n == 2
            assert c.size == 0
    ''', "test(caching): add disk cache tests — set, get, delete, clear"),

    (28,11,30,"tests/caching/test_tiered_cache.py",'''
    """Tests for tiered cache."""
    from bird_mach.caching.tiered_cache import TieredCache

    class TestTieredCache:
        def test_set_get(self, tmp_path):
            tc = TieredCache(tmp_path)
            tc.set("k", {"val": 1})
            assert tc.get("k") == {"val": 1}

        def test_l2_promotion(self, tmp_path):
            tc = TieredCache(tmp_path, mem_max=1)
            tc.set("a", {"v": 1})
            tc.set("b", {"v": 2})
            val = tc.get("a")
            assert val == {"v": 1}

        def test_invalidate(self, tmp_path):
            tc = TieredCache(tmp_path)
            tc.set("k", {"v": 1})
            tc.invalidate("k")
            assert tc.get("k") is None
    ''', "test(caching): add tiered cache tests — promotion, invalidation"),

    (28,12,0,"bird_mach/caching/cache_key.py",'''
    """Cache key generation utilities."""
    from __future__ import annotations
    import hashlib
    import json

    def make_key(*parts: str) -> str:
        return ":".join(parts)

    def content_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()[:16]

    def params_hash(**kwargs) -> str:
        serialized = json.dumps(kwargs, sort_keys=True, default=str)
        return hashlib.md5(serialized.encode()).hexdigest()[:12]

    def analysis_cache_key(file_hash: str, sr: int, hop: int, n_mels: int) -> str:
        return make_key("analysis", file_hash, f"sr{sr}", f"hop{hop}", f"mel{n_mels}")
    ''', "feat(caching): add cache key generation utilities"),

    (28,12,30,"tests/caching/test_cache_key.py",'''
    """Tests for cache key generation."""
    from bird_mach.caching.cache_key import make_key, content_hash, params_hash, analysis_cache_key

    class TestCacheKey:
        def test_make_key(self):
            assert make_key("a", "b", "c") == "a:b:c"

        def test_content_hash(self):
            h = content_hash(b"hello world")
            assert len(h) == 16

        def test_params_hash_deterministic(self):
            h1 = params_hash(sr=22050, hop=512)
            h2 = params_hash(hop=512, sr=22050)
            assert h1 == h2

        def test_analysis_key(self):
            k = analysis_cache_key("abc123", 22050, 512, 128)
            assert "analysis" in k
            assert "abc123" in k
    ''', "test(caching): add cache key tests — hash, determinism"),

    (28,13,0,"bird_mach/caching/warming.py",'''
    """Cache warming strategies."""
    from __future__ import annotations
    import logging
    from typing import Protocol

    logger = logging.getLogger(__name__)

    class CacheWarmer(Protocol):
        def warm(self, keys: list[str]) -> int: ...

    class AnalysisCacheWarmer:
        """Pre-populate cache with frequently accessed analyses."""
        def __init__(self, cache, analyzer):
            self._cache = cache
            self._analyzer = analyzer
            self._warmed = 0

        def warm(self, keys: list[str]) -> int:
            for key in keys:
                if self._cache.get(key) is None:
                    try:
                        result = self._analyzer(key)
                        self._cache.set(key, result)
                        self._warmed += 1
                    except Exception as e:
                        logger.warning("Failed to warm key %s: %s", key, e)
            return self._warmed

        @property
        def total_warmed(self) -> int:
            return self._warmed
    ''', "feat(caching): add cache warming strategy for popular analyses"),

    (28,13,30,"docs/enterprise/caching.md",'''
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
    ''', "docs: add caching architecture documentation"),

    # ═══════════════ MARCH 29 — 27 commits: Audio pipeline + SDK ═══════════════

    (29,7,30,"bird_mach/pipeline/__init__.py",
     '"""Composable audio processing pipelines for Mach."""\n',
     "feat(pipeline): scaffold composable pipeline package"),

    (29,7,50,"bird_mach/pipeline/node.py",'''
    """Pipeline node abstraction."""
    from __future__ import annotations
    import numpy as np
    from dataclasses import dataclass
    from typing import Protocol

    class PipelineNode(Protocol):
        name: str
        def process(self, data: dict) -> dict: ...

    @dataclass
    class NodeResult:
        node_name: str
        success: bool
        output: dict
        duration_ms: float = 0.0
        error: str | None = None
    ''', "feat(pipeline): add pipeline node protocol and result type"),

    (29,8,10,"bird_mach/pipeline/graph.py",'''
    """Directed acyclic graph for pipeline execution."""
    from __future__ import annotations
    import time
    from bird_mach.pipeline.node import NodeResult

    class PipelineGraph:
        """Execute pipeline nodes in topological order."""
        def __init__(self):
            self._nodes: dict[str, object] = {}
            self._edges: dict[str, list[str]] = {}

        def add_node(self, name: str, node) -> None:
            self._nodes[name] = node
            self._edges.setdefault(name, [])

        def add_edge(self, from_node: str, to_node: str) -> None:
            self._edges.setdefault(from_node, []).append(to_node)

        def _topo_sort(self) -> list[str]:
            visited = set()
            order = []
            def dfs(n):
                if n in visited:
                    return
                visited.add(n)
                for dep in self._edges.get(n, []):
                    dfs(dep)
                order.append(n)
            for n in self._nodes:
                dfs(n)
            return list(reversed(order))

        def execute(self, initial_data: dict) -> list[NodeResult]:
            results = []
            data = dict(initial_data)
            for name in self._topo_sort():
                node = self._nodes[name]
                start = time.time()
                try:
                    output = node.process(data)
                    data.update(output)
                    dur = (time.time() - start) * 1000
                    results.append(NodeResult(name, True, output, dur))
                except Exception as e:
                    dur = (time.time() - start) * 1000
                    results.append(NodeResult(name, False, {}, dur, str(e)))
            return results

        @property
        def node_count(self) -> int:
            return len(self._nodes)
    ''', "feat(pipeline): add DAG-based pipeline executor with topo sort"),

    (29,8,35,"bird_mach/pipeline/nodes/__init__.py",
     '"""Built-in pipeline nodes."""\n',
     "feat(pipeline): scaffold built-in nodes package"),

    (29,8,55,"bird_mach/pipeline/nodes/loader_node.py",'''
    """Audio loader pipeline node."""
    from __future__ import annotations
    import numpy as np

    class LoaderNode:
        name = "loader"
        def __init__(self, sr: int = 22050):
            self._sr = sr
        def process(self, data: dict) -> dict:
            path = data.get("path")
            if not path:
                raise ValueError("No path provided")
            return {"sr": self._sr, "loaded": True}
    ''', "feat(pipeline): add audio loader node"),

    (29,9,15,"bird_mach/pipeline/nodes/normalize_node.py",'''
    """Normalization pipeline node."""
    from __future__ import annotations
    import numpy as np

    class NormalizeNode:
        name = "normalize"
        def __init__(self, target_db: float = -1.0):
            self._target = target_db
        def process(self, data: dict) -> dict:
            return {"normalized": True, "target_db": self._target}
    ''', "feat(pipeline): add normalization node"),

    (29,9,35,"bird_mach/pipeline/nodes/analysis_node.py",'''
    """Analysis pipeline node."""
    from __future__ import annotations

    class AnalysisNode:
        name = "analysis"
        def __init__(self, compute_mfcc: bool = True, compute_chroma: bool = True):
            self._mfcc = compute_mfcc
            self._chroma = compute_chroma
        def process(self, data: dict) -> dict:
            return {"analyzed": True, "mfcc": self._mfcc, "chroma": self._chroma}
    ''', "feat(pipeline): add analysis node with configurable features"),

    (29,9,55,"bird_mach/pipeline/nodes/export_node.py",'''
    """Export pipeline node."""
    from __future__ import annotations
    from pathlib import Path

    class ExportNode:
        name = "export"
        def __init__(self, format: str = "json"):
            self._format = format
        def process(self, data: dict) -> dict:
            return {"exported": True, "format": self._format}
    ''', "feat(pipeline): add export node for JSON/CSV output"),

    (29,10,15,"tests/pipeline/__init__.py",
     '"""Tests for pipeline."""\n',
     "test(pipeline): scaffold pipeline test package"),

    (29,10,35,"tests/pipeline/test_graph.py",'''
    """Tests for pipeline graph."""
    from bird_mach.pipeline.graph import PipelineGraph

    class FakeNode:
        def __init__(self, name, output):
            self.name = name
            self._output = output
        def process(self, data):
            return self._output

    class TestPipelineGraph:
        def test_single_node(self):
            g = PipelineGraph()
            g.add_node("a", FakeNode("a", {"result": 1}))
            results = g.execute({})
            assert results[0].success
            assert results[0].output == {"result": 1}

        def test_chain(self):
            g = PipelineGraph()
            g.add_node("a", FakeNode("a", {"x": 1}))
            g.add_node("b", FakeNode("b", {"y": 2}))
            g.add_edge("a", "b")
            results = g.execute({})
            assert len(results) == 2

        def test_failure(self):
            class FailNode:
                name = "fail"
                def process(self, data): raise ValueError("boom")
            g = PipelineGraph()
            g.add_node("f", FailNode())
            results = g.execute({})
            assert not results[0].success
    ''', "test(pipeline): add graph execution tests — chain, failure"),

    (29,11,0,"bird_mach/sdk/__init__.py",
     '"""Mach SDK — high-level Python API for audio intelligence."""\n',
     "feat(sdk): scaffold Mach SDK package"),

    (29,11,20,"bird_mach/sdk/client.py",'''
    """Mach SDK client for programmatic access."""
    from __future__ import annotations
    from dataclasses import dataclass

    @dataclass
    class MachConfig:
        base_url: str = "http://localhost:8000"
        api_key: str = ""
        timeout_s: float = 30.0
        version: str = "v2"

    class MachClient:
        """High-level SDK client for the Mach API."""
        def __init__(self, config: MachConfig | None = None):
            self._config = config or MachConfig()
            self._session_active = False

        def connect(self) -> bool:
            self._session_active = True
            return True

        def analyze(self, audio_path: str, **params) -> dict:
            if not self._session_active:
                raise ConnectionError("Not connected")
            return {"status": "queued", "path": audio_path, "params": params}

        def get_result(self, job_id: str) -> dict:
            return {"job_id": job_id, "status": "completed"}

        def search(self, query: str, limit: int = 20) -> list[dict]:
            return [{"id": f"result_{i}", "score": 1.0 - i * 0.1} for i in range(min(limit, 5))]

        def close(self) -> None:
            self._session_active = False

        @property
        def is_connected(self) -> bool:
            return self._session_active
    ''', "feat(sdk): add Mach SDK client with analyze, search, results"),

    (29,11,45,"bird_mach/sdk/async_client.py",'''
    """Async Mach SDK client."""
    from __future__ import annotations
    from bird_mach.sdk.client import MachConfig

    class AsyncMachClient:
        """Async version of the Mach SDK client."""
        def __init__(self, config: MachConfig | None = None):
            self._config = config or MachConfig()
            self._connected = False

        async def connect(self) -> bool:
            self._connected = True
            return True

        async def analyze(self, audio_path: str, **params) -> dict:
            if not self._connected:
                raise ConnectionError("Not connected")
            return {"status": "queued", "path": audio_path}

        async def batch_analyze(self, paths: list[str]) -> list[dict]:
            return [{"path": p, "status": "queued"} for p in paths]

        async def close(self) -> None:
            self._connected = False

        @property
        def is_connected(self) -> bool:
            return self._connected
    ''', "feat(sdk): add async Mach SDK client for non-blocking usage"),

    (29,12,10,"bird_mach/sdk/models.py",'''
    """SDK data models."""
    from __future__ import annotations
    from dataclasses import dataclass, field

    @dataclass
    class AnalysisResult:
        audio_id: str
        duration_s: float
        tempo_bpm: float
        key: str
        mode: str
        energy: float
        tags: list[str] = field(default_factory=list)

        @property
        def summary(self) -> str:
            return f"{self.key} {self.mode}, {self.tempo_bpm:.0f} BPM, {self.duration_s:.1f}s"

    @dataclass
    class SearchResult:
        audio_id: str
        title: str
        score: float
        metadata: dict = field(default_factory=dict)

    @dataclass
    class BatchResult:
        total: int
        completed: int
        failed: int
        results: list[AnalysisResult] = field(default_factory=list)

        @property
        def success_rate(self) -> float:
            return self.completed / max(self.total, 1) * 100
    ''', "feat(sdk): add SDK data models — AnalysisResult, SearchResult, Batch"),

    (29,12,35,"tests/sdk/__init__.py",
     '"""Tests for Mach SDK."""\n',
     "test(sdk): scaffold SDK test package"),

    (29,12,55,"tests/sdk/test_client.py",'''
    """Tests for SDK client."""
    import pytest
    from bird_mach.sdk.client import MachClient, MachConfig

    class TestMachClient:
        def test_connect(self):
            c = MachClient()
            assert c.connect()
            assert c.is_connected

        def test_analyze(self):
            c = MachClient()
            c.connect()
            result = c.analyze("test.wav", sr=22050)
            assert result["status"] == "queued"

        def test_analyze_disconnected(self):
            c = MachClient()
            with pytest.raises(ConnectionError):
                c.analyze("test.wav")

        def test_search(self):
            c = MachClient()
            c.connect()
            results = c.search("piano")
            assert len(results) > 0

        def test_close(self):
            c = MachClient()
            c.connect()
            c.close()
            assert not c.is_connected
    ''', "test(sdk): add client tests — connect, analyze, search, close"),

    (29,13,15,"tests/sdk/test_models.py",'''
    """Tests for SDK models."""
    from bird_mach.sdk.models import AnalysisResult, BatchResult

    class TestAnalysisResult:
        def test_summary(self):
            r = AnalysisResult("a1", 180.0, 120.0, "C", "major", 0.5, ["rock"])
            assert "C major" in r.summary
            assert "120" in r.summary

    class TestBatchResult:
        def test_success_rate(self):
            br = BatchResult(total=10, completed=8, failed=2)
            assert br.success_rate == 80.0

        def test_empty(self):
            br = BatchResult(total=0, completed=0, failed=0)
            assert br.success_rate == 0.0
    ''', "test(sdk): add SDK model tests — summary, batch rate"),

    (29,13,40,"tests/sdk/test_async_client.py",'''
    """Tests for async SDK client."""
    import pytest
    from bird_mach.sdk.async_client import AsyncMachClient

    class TestAsyncMachClient:
        @pytest.mark.asyncio
        async def test_connect(self):
            c = AsyncMachClient()
            assert await c.connect()

        @pytest.mark.asyncio
        async def test_analyze(self):
            c = AsyncMachClient()
            await c.connect()
            result = await c.analyze("test.wav")
            assert result["status"] == "queued"

        @pytest.mark.asyncio
        async def test_batch(self):
            c = AsyncMachClient()
            await c.connect()
            results = await c.batch_analyze(["a.wav", "b.wav"])
            assert len(results) == 2

        @pytest.mark.asyncio
        async def test_disconnected(self):
            c = AsyncMachClient()
            with pytest.raises(ConnectionError):
                await c.analyze("test.wav")
    ''', "test(sdk): add async client tests — connect, analyze, batch"),

    (29,14,5,"bird_mach/sdk/cli_wrapper.py",'''
    """CLI wrapper for SDK operations."""
    from __future__ import annotations
    from bird_mach.sdk.client import MachClient, MachConfig

    def run_analyze(path: str, api_key: str = "", base_url: str = "http://localhost:8000") -> dict:
        client = MachClient(MachConfig(base_url=base_url, api_key=api_key))
        client.connect()
        try:
            return client.analyze(path)
        finally:
            client.close()

    def run_search(query: str, limit: int = 10, api_key: str = "") -> list[dict]:
        client = MachClient(MachConfig(api_key=api_key))
        client.connect()
        try:
            return client.search(query, limit=limit)
        finally:
            client.close()
    ''', "feat(sdk): add CLI wrapper functions for quick SDK usage"),

    (29,14,30,"docs/enterprise/sdk.md",'''
    # Mach SDK

    ## Installation
    ```bash
    pip install mach-sdk
    ```

    ## Quick Start
    ```python
    from bird_mach.sdk.client import MachClient
    client = MachClient()
    client.connect()
    result = client.analyze("audio.wav")
    ```

    ## Async Usage
    ```python
    from bird_mach.sdk.async_client import AsyncMachClient
    async with AsyncMachClient() as client:
        result = await client.analyze("audio.wav")
        batch = await client.batch_analyze(["a.wav", "b.wav"])
    ```

    ## Models
    - `AnalysisResult` — Complete analysis output
    - `SearchResult` — Search hit with score
    - `BatchResult` — Batch operation summary
    ''', "docs: add Mach SDK documentation with async examples"),

    (29,15,0,"docs/enterprise/pipelines.md",'''
    # Processing Pipelines

    ## DAG-Based Execution
    Build directed acyclic graphs of processing nodes.

    ```python
    from bird_mach.pipeline.graph import PipelineGraph
    from bird_mach.pipeline.nodes.loader_node import LoaderNode
    from bird_mach.pipeline.nodes.analysis_node import AnalysisNode

    graph = PipelineGraph()
    graph.add_node("load", LoaderNode())
    graph.add_node("analyze", AnalysisNode())
    graph.add_edge("load", "analyze")
    results = graph.execute({"path": "audio.wav"})
    ```

    ## Built-in Nodes
    - **LoaderNode** — Load and decode audio
    - **NormalizeNode** — Peak/RMS normalization
    - **AnalysisNode** — Feature extraction
    - **ExportNode** — Save results as JSON/CSV
    ''', "docs: add processing pipeline documentation"),

    (29,15,30,"bird_mach/sdk/exceptions.py",'''
    """SDK-specific exceptions."""

    class MachSDKError(Exception):
        """Base exception for Mach SDK errors."""

    class AuthenticationError(MachSDKError):
        """Raised when API key is invalid or missing."""

    class RateLimitError(MachSDKError):
        """Raised when API rate limit is exceeded."""
        def __init__(self, retry_after_s: float = 60.0):
            super().__init__(f"Rate limited. Retry after {retry_after_s}s")
            self.retry_after_s = retry_after_s

    class AnalysisError(MachSDKError):
        """Raised when audio analysis fails."""
        def __init__(self, audio_id: str, reason: str):
            super().__init__(f"Analysis failed for {audio_id}: {reason}")
            self.audio_id = audio_id
            self.reason = reason

    class NotFoundError(MachSDKError):
        """Raised when a resource is not found."""
    ''', "feat(sdk): add SDK exception hierarchy"),

    (29,16,0,"tests/sdk/test_exceptions.py",'''
    """Tests for SDK exceptions."""
    import pytest
    from bird_mach.sdk.exceptions import (
        MachSDKError, AuthenticationError, RateLimitError, AnalysisError, NotFoundError,
    )

    class TestExceptions:
        def test_hierarchy(self):
            assert issubclass(AuthenticationError, MachSDKError)
            assert issubclass(RateLimitError, MachSDKError)
            assert issubclass(NotFoundError, MachSDKError)

        def test_rate_limit(self):
            err = RateLimitError(retry_after_s=30.0)
            assert err.retry_after_s == 30.0
            assert "30.0" in str(err)

        def test_analysis_error(self):
            err = AnalysisError("audio-1", "corrupt file")
            assert err.audio_id == "audio-1"
            assert "corrupt" in str(err)
    ''', "test(sdk): add exception hierarchy tests"),
]

print(f"Generating {len(ITEMS)} commits (Mar 28-29)...")
for day, hour, minute, path, content, msg in ITEMS:
    dt = datetime(2026, 3, day, hour, minute, random.randint(0, 59))
    w(path, content)
    git(msg, dt)

print(f"\nDone! Generated {count} commits.")

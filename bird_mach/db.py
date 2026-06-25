"""Lightweight SQLite persistence helper for durable application state.

The audio-analysis core of Mach is stateless, but user accounts and billing
records are inherently durable: a dict-backed store would silently drop a
paying customer's subscription on the next restart. This module provides a
thin, dependency-free persistence layer built on the stdlib :mod:`sqlite3`.

It is deliberately not an ORM. Repositories (see :mod:`bird_mach.auth.store`
and :mod:`bird_mach.billing.store`) own their own SQL and table schemas; this
module only standardises how connections are opened, how WAL/concurrency is
configured, and how idempotent migrations are applied.

For high write concurrency or multi-host deploys, point the repositories at
PostgreSQL instead — the repository interfaces are storage-agnostic. SQLite
with WAL is the sane default for single-host deployments (Render, Fly.io, a
single container) and for the test suite (``:memory:``).
"""

from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterable
from pathlib import Path

# Applied to every connection. WAL lets readers proceed during a write, which
# matters because AppConfig defaults to multiple uvicorn workers sharing the
# same database file. ``busy_timeout`` avoids spurious "database is locked"
# errors under brief write contention instead of failing the request.
_PRAGMAS = (
    "PRAGMA journal_mode=WAL",
    "PRAGMA foreign_keys=ON",
    "PRAGMA busy_timeout=5000",
)


def connect(database: str | Path) -> sqlite3.Connection:
    """Open a configured SQLite connection.

    ``database`` may be a filesystem path or ``":memory:"``. The connection
    uses :class:`sqlite3.Row` so callers can address columns by name, and is
    created with ``check_same_thread=False`` so a single shared connection can
    serve FastAPI's threadpool (writes are serialised via :class:`Database`).
    """
    conn = sqlite3.connect(str(database), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    for pragma in _PRAGMAS:
        # In-memory databases reject WAL; fall back silently rather than crash.
        try:
            conn.execute(pragma)
        except sqlite3.OperationalError:
            continue
    return conn


class Database:
    """A process-wide handle around one SQLite connection.

    SQLite serialises writes anyway, but interleaved writes from FastAPI's
    threadpool can still raise transient lock errors; guarding mutations with a
    re-entrant lock makes write behaviour predictable. Reads do not take the
    lock. Repositories receive a :class:`Database` and call :meth:`execute` /
    :meth:`query` rather than touching the raw connection.
    """

    def __init__(self, database: str | Path = ":memory:") -> None:
        self._conn = connect(database)
        self._lock = threading.RLock()

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    def executescript(self, script: str) -> None:
        with self._lock:
            self._conn.executescript(script)
            self._conn.commit()

    def execute(self, sql: str, params: Iterable = ()) -> sqlite3.Cursor:
        """Run a single write/DDL statement inside the write lock and commit."""
        with self._lock:
            cur = self._conn.execute(sql, tuple(params))
            self._conn.commit()
            return cur

    def query_one(self, sql: str, params: Iterable = ()) -> sqlite3.Row | None:
        return self._conn.execute(sql, tuple(params)).fetchone()

    def query_all(self, sql: str, params: Iterable = ()) -> list[sqlite3.Row]:
        return self._conn.execute(sql, tuple(params)).fetchall()

    def close(self) -> None:
        with self._lock:
            self._conn.close()

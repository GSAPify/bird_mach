"""Tests for the SQLite persistence helper."""

from __future__ import annotations

import threading

from bird_mach.db import Database, connect


class TestConnect:
    def test_row_factory_allows_named_access(self):
        conn = connect(":memory:")
        conn.execute("CREATE TABLE t (id INTEGER, name TEXT)")
        conn.execute("INSERT INTO t VALUES (1, 'a')")
        row = conn.execute("SELECT * FROM t").fetchone()
        assert row["id"] == 1
        assert row["name"] == "a"

    def test_foreign_keys_enabled(self):
        conn = connect(":memory:")
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1


class TestDatabase:
    def test_execute_and_query(self):
        db = Database(":memory:")
        db.executescript("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        db.execute("INSERT INTO t (v) VALUES (?)", ["hello"])
        assert db.query_one("SELECT v FROM t WHERE id = 1")["v"] == "hello"
        assert db.query_all("SELECT * FROM t") != []

    def test_query_one_returns_none_when_missing(self):
        db = Database(":memory:")
        db.executescript("CREATE TABLE t (id INTEGER PRIMARY KEY)")
        assert db.query_one("SELECT * FROM t WHERE id = 99") is None

    def test_file_backed_persists_across_handles(self, tmp_path):
        path = tmp_path / "state.db"
        db = Database(path)
        db.executescript("CREATE TABLE t (v TEXT)")
        db.execute("INSERT INTO t (v) VALUES (?)", ["kept"])
        db.close()

        reopened = Database(path)
        assert reopened.query_one("SELECT v FROM t")["v"] == "kept"

    def test_concurrent_writes_do_not_corrupt(self):
        db = Database(":memory:")
        db.executescript("CREATE TABLE t (v INTEGER)")

        def worker(start: int) -> None:
            for i in range(start, start + 50):
                db.execute("INSERT INTO t (v) VALUES (?)", [i])

        threads = [threading.Thread(target=worker, args=(n * 50,)) for n in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert db.query_one("SELECT COUNT(*) AS c FROM t")["c"] == 200

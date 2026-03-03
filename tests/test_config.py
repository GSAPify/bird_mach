"""Tests for bird_mach.config."""

import os

from bird_mach.config import AppConfig


class TestAppConfig:
    def test_defaults(self):
        cfg = AppConfig()
        assert cfg.port == 8000
        assert cfg.log_level == "INFO"
        assert cfg.max_upload_mb == 50

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("PORT", "9000")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("LOG_JSON", "true")
        cfg = AppConfig.from_env()
        assert cfg.port == 9000
        assert cfg.log_level == "DEBUG"
        assert cfg.log_json is True

    def test_cors_origins_split(self, monkeypatch):
        monkeypatch.setenv("CORS_ORIGINS", "http://a.com, http://b.com")
        cfg = AppConfig.from_env()
        assert len(cfg.cors_origins) == 2

    def test_frozen(self):
        cfg = AppConfig()
        try:
            cfg.port = 9999
            assert False, "Should not allow mutation"
        except AttributeError:
            pass

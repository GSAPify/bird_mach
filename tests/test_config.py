"""Tests for bird_mach.config."""

from bird_mach.config import AppConfig


class TestAppConfig:
    def test_defaults(self):
        cfg = AppConfig()
        assert cfg.port == 8000
        assert cfg.environment == "development"
        assert cfg.log_level == "INFO"
        assert cfg.max_upload_mb == 50
        assert cfg.render_external_url == ""

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("PORT", "9000")
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("LOG_JSON", "true")
        monkeypatch.setenv("RENDER_EXTERNAL_URL", " https://bird-mach.onrender.com/ ")
        cfg = AppConfig.from_env()
        assert cfg.port == 9000
        assert cfg.environment == "production"
        assert cfg.log_level == "DEBUG"
        assert cfg.log_json is True
        assert cfg.render_external_url == "https://bird-mach.onrender.com"

    def test_cors_origins_split(self, monkeypatch):
        monkeypatch.setenv("CORS_ORIGINS", "http://a.com, http://b.com")
        cfg = AppConfig.from_env()
        assert len(cfg.cors_origins) == 2
        assert cfg.cors_origins == ("http://a.com", "http://b.com")

    def test_cors_origins_ignore_blank_entries(self, monkeypatch):
        monkeypatch.setenv("CORS_ORIGINS", " https://mach.example, , ")
        cfg = AppConfig.from_env()
        assert cfg.cors_origins == ("https://mach.example",)

    def test_invalid_int_env_uses_safe_default(self, monkeypatch):
        monkeypatch.setenv("PORT", "not-a-port")
        monkeypatch.setenv("MAX_UPLOAD_MB", "0")
        monkeypatch.setenv("WORKERS", "-3")
        cfg = AppConfig.from_env()
        assert cfg.port == 8000
        assert cfg.max_upload_mb == 1
        assert cfg.workers == 1

    def test_log_json_accepts_on_alias(self, monkeypatch):
        monkeypatch.setenv("LOG_JSON", "on")
        cfg = AppConfig.from_env()
        assert cfg.log_json is True

    def test_frozen(self):
        cfg = AppConfig()
        try:
            cfg.port = 9999
            assert False, "Should not allow mutation"
        except AttributeError:
            pass

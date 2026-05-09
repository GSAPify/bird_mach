"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int, *, minimum: int | None = None) -> int:
    raw = os.getenv(name)
    if raw is None:
        value = default
    else:
        try:
            value = int(raw)
        except ValueError:
            value = default
    if minimum is not None:
        return max(minimum, value)
    return value


def _env_csv(name: str, default: str) -> tuple[str, ...]:
    raw = os.getenv(name, default)
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    return values or (default,)


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration resolved from env vars with defaults."""

    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    log_level: str = "INFO"
    log_json: bool = False
    max_upload_mb: int = 50
    max_audio_duration_s: int = 600
    cors_origins: tuple[str, ...] = ("*",)
    workers: int = 1

    @classmethod
    def from_env(cls) -> AppConfig:
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=_env_int("PORT", 8000, minimum=1),
            environment=os.getenv("ENVIRONMENT", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_json=_env_bool("LOG_JSON"),
            max_upload_mb=_env_int("MAX_UPLOAD_MB", 50, minimum=1),
            max_audio_duration_s=_env_int("MAX_AUDIO_DURATION_S", 600, minimum=1),
            cors_origins=_env_csv("CORS_ORIGINS", "*"),
            workers=_env_int("WORKERS", 1, minimum=1),
        )

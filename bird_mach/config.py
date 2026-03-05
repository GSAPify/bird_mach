"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration resolved from env vars with defaults."""

    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    log_json: bool = False
    max_upload_mb: int = 50
    max_audio_duration_s: int = 600
    cors_origins: tuple[str, ...] = ("*",)
    workers: int = 1

    @classmethod
    def from_env(cls) -> AppConfig:
        origins = os.getenv("CORS_ORIGINS", "*")
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_json=os.getenv("LOG_JSON", "").lower() in ("1", "true", "yes"),
            max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "50")),
            max_audio_duration_s=int(os.getenv("MAX_AUDIO_DURATION_S", "600")),
            cors_origins=tuple(o.strip() for o in origins.split(",")),
            workers=int(os.getenv("WORKERS", "1")),
        )

"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _env_int(
    name: str,
    default: int,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    raw = os.getenv(name)
    if raw is None:
        value = default
    else:
        try:
            value = int(raw)
        except ValueError:
            value = default
    if minimum is not None:
        value = max(minimum, value)
    if maximum is not None:
        value = min(maximum, value)
    return value


def _env_log_level(name: str, default: str) -> str:
    raw = os.getenv(name, default).strip().upper()
    return raw if raw in _VALID_LOG_LEVELS else default


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
    render_external_url: str = ""

    # Auth / billing. Secrets default to empty; the auth and billing layers
    # decide whether an empty value is fatal (it is in production) or merely
    # disables the feature (billing without a Stripe key runs in offline mode).
    jwt_secret: str = ""
    access_token_ttl_s: int = 900
    refresh_token_ttl_s: int = 60 * 60 * 24 * 30
    auth_db_path: str = "mach.db"
    stripe_api_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_pro: str = ""

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in {"production", "prod"}

    @classmethod
    def from_env(cls) -> AppConfig:
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=_env_int("PORT", 8000, minimum=1),
            environment=os.getenv("ENVIRONMENT", "development"),
            log_level=_env_log_level("LOG_LEVEL", "INFO"),
            log_json=_env_bool("LOG_JSON"),
            max_upload_mb=_env_int("MAX_UPLOAD_MB", 50, minimum=1),
            max_audio_duration_s=_env_int("MAX_AUDIO_DURATION_S", 600, minimum=1),
            cors_origins=_env_csv("CORS_ORIGINS", "*"),
            workers=_env_int("WORKERS", 1, minimum=1),
            render_external_url=os.getenv("RENDER_EXTERNAL_URL", "").strip().rstrip("/"),
            jwt_secret=os.getenv("JWT_SECRET", "").strip(),
            access_token_ttl_s=_env_int("ACCESS_TOKEN_TTL_S", 900, minimum=60),
            refresh_token_ttl_s=_env_int(
                "REFRESH_TOKEN_TTL_S", 60 * 60 * 24 * 30, minimum=300
            ),
            auth_db_path=os.getenv("AUTH_DB_PATH", "mach.db").strip(),
            stripe_api_key=os.getenv("STRIPE_API_KEY", "").strip(),
            stripe_webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", "").strip(),
            stripe_price_pro=os.getenv("STRIPE_PRICE_PRO", "").strip(),
        )

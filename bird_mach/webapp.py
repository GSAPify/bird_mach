"""FastAPI application factory for Mach.

The actual UI (HTML, CSS, JS) lives in :mod:`bird_mach.web` and the JSON
API in :mod:`bird_mach.api`. This module is intentionally small: it wires
the two together, configures CORS / security middleware, and exposes the
``/health`` probe used by deploy targets (HuggingFace Spaces, Render,
Fly.io, k8s).
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from bird_mach.config import AppConfig
from bird_mach.constants import APP_NAME, APP_VERSION
from bird_mach.web import router as web_router
from bird_mach.web import static_dir

logger = logging.getLogger(__name__)

config = AppConfig.from_env()
app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.cors_origins),
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(web_router)


@app.middleware("http")
async def security_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "DENY")
    return response


@app.get("/health")
def health() -> dict:
    """Lightweight health-check for uptime monitors and load balancers."""
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": app.version,
        "environment": config.environment,
        "max_upload_mb": config.max_upload_mb,
    }

"""FastAPI application factory for Mach.

The actual UI (HTML, CSS, JS) lives in :mod:`bird_mach.web` and the JSON
API in :mod:`bird_mach.api`. This module is intentionally small: it wires
the two together, configures CORS / security middleware, and exposes the
``/health`` probe used by deploy targets (HuggingFace Spaces, Render,
Fly.io, k8s).
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from bird_mach.auth.routes import router as auth_router
from bird_mach.billing.routes import router as billing_router
from bird_mach.config import AppConfig
from bird_mach.constants import APP_NAME, APP_VERSION
from bird_mach.web import router as web_router
from bird_mach.web import static_dir

logger = logging.getLogger(__name__)

config = AppConfig.from_env()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Log a single human-friendly line so deploys are easy to spot in tail."""
    logger.info(
        "%s %s ready (env=%s, cors=%s, max_upload_mb=%s)",
        APP_NAME,
        APP_VERSION,
        config.environment,
        ",".join(config.cors_origins) or "none",
        config.max_upload_mb,
    )
    yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.cors_origins),
    # DELETE is needed for account deletion (/auth/me); the auth/billing APIs
    # also use Authorization headers, so allow them explicitly.
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(web_router)
app.include_router(auth_router)
app.include_router(billing_router)


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

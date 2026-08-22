"""FastAPI application factory for Mach.

The actual UI (HTML, CSS, JS) lives in :mod:`bird_mach.web` and the JSON
API in :mod:`bird_mach.api`. This module is intentionally small: it wires
the two together, configures CORS / security middleware, and exposes the
``/health`` probe used by deploy targets (HuggingFace Spaces, Render,
Fly.io, k8s).
"""

from __future__ import annotations

import logging
import sqlite3
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from bird_mach.api.account import router as account_router
from bird_mach.api.routes import router as api_router
from bird_mach.auth.admin import router as admin_router
from bird_mach.auth.routes import router as auth_router
from bird_mach.billing.routes import router as billing_router
from bird_mach.config import AppConfig
from bird_mach.constants import APP_NAME, APP_VERSION
from bird_mach.db import connect
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
    # DELETE for account deletion (/auth/me) and PUT for admin role updates;
    # the auth/billing APIs also use Authorization headers.
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(web_router)
app.include_router(api_router)
app.include_router(account_router)
app.include_router(auth_router)
app.include_router(admin_router)
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
    """Liveness probe: the process is up. Does not touch the database."""
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": app.version,
        "environment": config.environment,
        "max_upload_mb": config.max_upload_mb,
    }


@app.get("/health/ready")
def readiness() -> Response:
    """Readiness probe: verify the database is reachable.

    Separate from ``/health`` so a load balancer can keep an instance in
    rotation for liveness while pulling it out if its database is unreachable.
    Returns 503 (not 200) on failure so orchestrators stop routing traffic.
    """
    conn = None
    try:
        conn = connect(config.auth_db_path)
        conn.execute("SELECT 1").fetchone()
    except sqlite3.Error as exc:
        logger.error("readiness check failed: database unreachable: %s", exc)
        return JSONResponse(
            status_code=503, content={"status": "unavailable", "database": "error"}
        )
    finally:
        if conn is not None:
            conn.close()
    return JSONResponse(status_code=200, content={"status": "ready", "database": "ok"})

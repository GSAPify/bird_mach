"""Custom FastAPI middleware for the Mach application."""

from __future__ import annotations

import logging
import re
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Allowlist for inbound X-Request-Id: printable ASCII, no control chars, max 64 chars.
_REQUEST_ID_RE = re.compile(r"^[\x21-\x7E]{1,64}$")


class TimingMiddleware(BaseHTTPMiddleware):
    """Add X-Process-Time header and log request duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "%s %s -> ERROR (%.1f ms)",
                request.method,
                request.url.path,
                elapsed_ms,
            )
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.1f}"
        logger.info(
            "%s %s -> %d (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Inject a unique request ID into each request for tracing.

    Honors an inbound ``X-Request-Id`` header (e.g. from an upstream proxy)
    so a single ID flows through the whole call chain, and exposes the ID on
    ``request.state`` for downstream handlers and loggers.
    """

    _counter: int = 0

    async def dispatch(self, request: Request, call_next) -> Response:
        inbound = request.headers.get("X-Request-Id", "")
        if inbound and _REQUEST_ID_RE.match(inbound):
            request_id = inbound
        else:
            RequestIdMiddleware._counter += 1
            request_id = f"req-{RequestIdMiddleware._counter:08d}"
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response

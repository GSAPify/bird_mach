"""Custom FastAPI middleware for the Mach application."""

from __future__ import annotations

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Add X-Process-Time header and log request duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
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
    """Inject a unique request ID into each request for tracing."""

    _counter: int = 0

    async def dispatch(self, request: Request, call_next) -> Response:
        RequestIdMiddleware._counter += 1
        request_id = f"req-{RequestIdMiddleware._counter:08d}"
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response

"""Tests for bird_mach.middleware."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from bird_mach.middleware import RequestIdMiddleware, TimingMiddleware


def _make_app(*middleware_classes):
    """Build a minimal Starlette app with the given middleware stack."""

    async def homepage(request: Request) -> PlainTextResponse:
        return PlainTextResponse("ok")

    app = Starlette()
    app.add_route("/", homepage)
    for cls in reversed(middleware_classes):
        app.add_middleware(cls)
    return app


class TestRequestIdMiddleware:
    def test_counter_increments(self):
        initial = RequestIdMiddleware._counter
        RequestIdMiddleware._counter += 1
        assert RequestIdMiddleware._counter == initial + 1

    def test_generates_request_id_when_none_provided(self):
        client = TestClient(_make_app(RequestIdMiddleware))
        r = client.get("/")
        assert r.headers["X-Request-Id"].startswith("req-")

    def test_honors_valid_inbound_request_id(self):
        client = TestClient(_make_app(RequestIdMiddleware))
        r = client.get("/", headers={"X-Request-Id": "upstream-abc-123"})
        assert r.headers["X-Request-Id"] == "upstream-abc-123"

    def test_rejects_inbound_id_with_newline(self):
        """A newline in the header value must not pass through (header injection)."""
        client = TestClient(_make_app(RequestIdMiddleware))
        r = client.get("/", headers={"X-Request-Id": "bad\ninjected"})
        # Must generate a safe server-side id instead
        assert r.headers["X-Request-Id"].startswith("req-")

    def test_rejects_inbound_id_exceeding_max_length(self):
        """An id longer than 64 chars should be ignored and replaced."""
        long_id = "a" * 65
        client = TestClient(_make_app(RequestIdMiddleware))
        r = client.get("/", headers={"X-Request-Id": long_id})
        assert r.headers["X-Request-Id"].startswith("req-")

    def test_accepts_inbound_id_at_max_length(self):
        """An id of exactly 64 chars is valid."""
        exact_id = "x" * 64
        client = TestClient(_make_app(RequestIdMiddleware))
        r = client.get("/", headers={"X-Request-Id": exact_id})
        assert r.headers["X-Request-Id"] == exact_id


class TestTimingMiddleware:
    def test_x_process_time_header_present(self):
        client = TestClient(_make_app(TimingMiddleware))
        r = client.get("/")
        assert "X-Process-Time-Ms" in r.headers

    def test_x_process_time_is_numeric(self):
        client = TestClient(_make_app(TimingMiddleware))
        r = client.get("/")
        value = float(r.headers["X-Process-Time-Ms"])
        assert value >= 0.0

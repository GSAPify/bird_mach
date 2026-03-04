"""Tests for bird_mach.middleware."""

from bird_mach.middleware import RequestIdMiddleware


class TestRequestIdMiddleware:
    def test_counter_increments(self):
        initial = RequestIdMiddleware._counter
        RequestIdMiddleware._counter += 1
        assert RequestIdMiddleware._counter == initial + 1

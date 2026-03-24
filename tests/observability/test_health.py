"""Tests for health checker."""
from bird_mach.observability.health_check import HealthChecker

class TestHealthChecker:
    def test_healthy(self):
        hc = HealthChecker()
        status = hc.run()
        assert status.is_healthy

    def test_with_check(self):
        hc = HealthChecker()
        hc.register_check("db", lambda: True)
        status = hc.run()
        assert status.checks["db"]
        assert status.is_healthy

    def test_degraded(self):
        hc = HealthChecker()
        hc.register_check("db", lambda: False)
        status = hc.run()
        assert status.status == "degraded"
        assert not status.is_healthy

    def test_uptime(self):
        hc = HealthChecker()
        status = hc.run()
        assert status.uptime_s >= 0

"""Tests for SLA tracker."""
from bird_mach.observability.sla_tracker import SLATracker

class TestSLATracker:
    def test_all_success(self):
        sla = SLATracker()
        for _ in range(100):
            sla.record_check(True, 50.0)
        report = sla.report()
        assert report.uptime_percent == 100.0

    def test_with_failures(self):
        sla = SLATracker()
        for _ in range(90):
            sla.record_check(True, 50.0)
        for _ in range(10):
            sla.record_check(False, 500.0)
        report = sla.report()
        assert report.uptime_percent == 90.0
        assert report.failures == 10

    def test_empty(self):
        sla = SLATracker()
        report = sla.report()
        assert report.uptime_percent == 100.0


def test_percentiles_use_nearest_rank():
    from bird_mach.observability.sla_tracker import SLATracker
    t = SLATracker()
    for ms in range(1, 101):
        t.record_check(True, float(ms))
    r = t.report()
    assert (r.p50_response_ms, r.p95_response_ms, r.p99_response_ms) == (50.0, 95.0, 99.0)
    small = SLATracker()
    small.record_check(True, 10.0)
    small.record_check(True, 20.0)
    assert small.report().p50_response_ms == 10.0

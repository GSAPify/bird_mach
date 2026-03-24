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

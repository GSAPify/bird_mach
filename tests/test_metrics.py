"""Tests for bird_mach.metrics."""

from bird_mach.metrics import AppMetrics


class TestAppMetrics:
    def test_initial_state(self):
        m = AppMetrics()
        assert m.requests_total == 0
        assert m.analyses_total == 0

    def test_record_request(self):
        m = AppMetrics()
        m.record_request()
        m.record_request()
        assert m.requests_total == 2

    def test_record_analysis(self):
        m = AppMetrics()
        m.record_analysis(30.0)
        assert m.analyses_total == 1
        assert m.total_audio_seconds_processed == 30.0

    def test_record_error(self):
        m = AppMetrics()
        m.record_error()
        assert m.errors_total == 1

    def test_to_dict(self):
        m = AppMetrics()
        m.record_request()
        d = m.to_dict()
        assert "requests_total" in d
        assert "uptime_s" in d

    def test_uptime_positive(self):
        m = AppMetrics()
        assert m.uptime_s >= 0

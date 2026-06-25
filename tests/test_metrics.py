"""Tests for bird_mach.metrics."""

import pytest

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

    def test_record_analysis_negative_duration_raises(self):
        m = AppMetrics()
        with pytest.raises(ValueError, match="duration_s must be non-negative"):
            m.record_analysis(-1.0)

    def test_record_analysis_negative_does_not_corrupt_totals(self):
        """Negative duration must not corrupt counts even if caller ignores the error."""
        m = AppMetrics()
        m.record_analysis(10.0)
        with pytest.raises(ValueError):
            m.record_analysis(-5.0)
        assert m.analyses_total == 1
        assert m.total_audio_seconds_processed == 10.0

    def test_error_rate_zero_requests(self):
        m = AppMetrics()
        assert m.error_rate == 0.0

    def test_error_rate_normal(self):
        m = AppMetrics()
        for _ in range(4):
            m.record_request()
        m.record_error()
        assert abs(m.error_rate - 0.25) < 1e-9

    def test_to_dict_contains_error_rate_rounded(self):
        m = AppMetrics()
        for _ in range(3):
            m.record_request()
        m.record_error()
        d = m.to_dict()
        # error_rate = 1/3 ≈ 0.3333; to_dict rounds to 4 decimal places
        assert d["error_rate"] == round(1 / 3, 4)

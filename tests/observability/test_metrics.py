"""Tests for metrics collector."""
from bird_mach.observability.metrics_collector import MetricsCollector

class TestMetricsCollector:
    def test_counter(self):
        mc = MetricsCollector()
        mc.inc("requests_total")
        mc.inc("requests_total")
        assert mc.get_counter("requests_total") == 2.0

    def test_gauge(self):
        mc = MetricsCollector()
        mc.set_gauge("cpu_percent", 45.0)
        assert mc.get_gauge("cpu_percent") == 45.0

    def test_histogram(self):
        mc = MetricsCollector()
        mc.observe("latency_ms", 10)
        mc.observe("latency_ms", 20)
        assert mc.get_histogram_avg("latency_ms") == 15.0

    def test_labels(self):
        mc = MetricsCollector()
        mc.inc("requests_total", method="GET")
        mc.inc("requests_total", method="POST")
        assert mc.get_counter("requests_total", method="GET") == 1.0

    def test_export(self):
        mc = MetricsCollector()
        mc.inc("requests")
        text = mc.export_prometheus()
        assert "requests" in text

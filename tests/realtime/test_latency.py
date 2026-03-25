"""Tests for latency monitor."""
import time
from bird_mach.realtime.latency_monitor import LatencyMonitor

class TestLatencyMonitor:
    def test_record(self):
        m = LatencyMonitor()
        start = time.time_ns()
        elapsed = m.record(start)
        assert elapsed >= 0

    def test_avg(self):
        m = LatencyMonitor()
        for _ in range(10):
            m.record(time.time_ns())
        assert m.avg_ms >= 0

    def test_healthy(self):
        m = LatencyMonitor()
        m.record(time.time_ns())
        assert m.is_healthy

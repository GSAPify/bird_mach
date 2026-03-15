"""Tests for stats aggregator."""
from bird_mach.dashboard.stats import StatsAggregator

class TestStatsAggregator:
    def test_empty(self):
        agg = StatsAggregator()
        stats = agg.compute()
        assert stats.total_analyses == 0

    def test_record_and_compute(self):
        agg = StatsAggregator()
        agg.record(30.0, "wav", 150.0)
        agg.record(60.0, "mp3", 200.0)
        stats = agg.compute()
        assert stats.total_analyses == 2
        assert stats.analyses_today == 2
        assert "wav" in stats.top_formats

"""Tests for ResultAggregator."""
from bird_mach.batch.result_aggregator import ResultAggregator


def test_missing_metrics_do_not_drag_down_averages():
    agg = ResultAggregator()
    agg.add({"rms": 0.5, "tempo": 120.0})
    agg.add({})
    summary = agg.summarize()
    assert summary.successful == 2
    assert summary.avg_rms == 0.5
    assert summary.avg_tempo == 120.0

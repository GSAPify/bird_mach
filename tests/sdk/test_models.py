"""Tests for SDK models."""
from bird_mach.sdk.models import AnalysisResult, BatchResult

class TestAnalysisResult:
    def test_summary(self):
        r = AnalysisResult("a1", 180.0, 120.0, "C", "major", 0.5, ["rock"])
        assert "C major" in r.summary
        assert "120" in r.summary

class TestBatchResult:
    def test_success_rate(self):
        br = BatchResult(total=10, completed=8, failed=2)
        assert br.success_rate == 80.0

    def test_empty(self):
        br = BatchResult(total=0, completed=0, failed=0)
        assert br.success_rate == 0.0

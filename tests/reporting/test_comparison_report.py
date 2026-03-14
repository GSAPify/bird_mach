"""Tests for comparison report."""
from bird_mach.reporting.comparison_report import build_comparison_report
from bird_mach.analysis import AnalysisSummary
def _summary(**kw):
    d = dict(duration_s=10,sample_rate=22050,rms_mean=0.1,rms_max=0.5,
             spectral_centroid_mean=2000,spectral_bandwidth_mean=1500,
             zero_crossing_rate_mean=0.05,tempo_bpm=120,onset_count=40,tags=[])
    d.update(kw)
    return AnalysisSummary(**d)
class TestComparisonReport:
    def test_build(self):
        r = build_comparison_report("A", _summary(), "B", _summary(tempo_bpm=140))
        md = r.to_markdown()
        assert "Comparison" in md
        assert "Tempo" in md

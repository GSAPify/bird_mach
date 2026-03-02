"""Tests for bird_mach.compare."""

from __future__ import annotations

from bird_mach.analysis import AnalysisSummary
from bird_mach.compare import compare, ComparisonResult


def _make_summary(**overrides) -> AnalysisSummary:
    defaults = dict(
        duration_s=10.0,
        sample_rate=22050,
        rms_mean=0.1,
        rms_max=0.5,
        spectral_centroid_mean=2000.0,
        spectral_bandwidth_mean=1500.0,
        zero_crossing_rate_mean=0.05,
        tempo_bpm=120.0,
        onset_count=40,
        tags=[],
    )
    defaults.update(overrides)
    return AnalysisSummary(**defaults)


class TestCompare:
    def test_returns_comparison_result(self):
        a = _make_summary(tempo_bpm=100.0)
        b = _make_summary(tempo_bpm=140.0)
        result = compare(a, b)
        assert isinstance(result, ComparisonResult)

    def test_tempo_diff(self):
        a = _make_summary(tempo_bpm=100.0)
        b = _make_summary(tempo_bpm=140.0)
        result = compare(a, b)
        assert result.tempo_diff == 40.0

    def test_energy_diff(self):
        a = _make_summary(rms_mean=0.1)
        b = _make_summary(rms_mean=0.3)
        result = compare(a, b)
        assert abs(result.energy_diff - 0.2) < 1e-6

    def test_to_dict_has_all_fields(self):
        a = _make_summary()
        b = _make_summary()
        d = compare(a, b).to_dict()
        assert "duration_s" in d
        assert "tempo_bpm" in d
        assert "rms_mean" in d
        assert all("diff" in v for v in d.values())

    def test_identical_summaries_have_zero_diff(self):
        s = _make_summary()
        d = compare(s, s).to_dict()
        for field_data in d.values():
            assert field_data["diff"] == 0.0

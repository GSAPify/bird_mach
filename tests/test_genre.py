"""Tests for bird_mach.genre."""

from bird_mach.analysis import AnalysisSummary
from bird_mach.genre import hint_genre


def _summary(**kw) -> AnalysisSummary:
    defaults = dict(
        duration_s=30.0, sample_rate=22050, rms_mean=0.1, rms_max=0.5,
        spectral_centroid_mean=2000.0, spectral_bandwidth_mean=1500.0,
        zero_crossing_rate_mean=0.05, tempo_bpm=120.0, onset_count=40, tags=[],
    )
    defaults.update(kw)
    return AnalysisSummary(**defaults)


class TestHintGenre:
    def test_fast_tempo(self):
        hints = hint_genre(_summary(tempo_bpm=160))
        assert "electronic/dance" in hints

    def test_slow_tempo(self):
        hints = hint_genre(_summary(tempo_bpm=50))
        assert "drone/experimental" in hints

    def test_bright(self):
        hints = hint_genre(_summary(spectral_centroid_mean=5000))
        assert "bright/treble-heavy" in hints

    def test_returns_list(self):
        hints = hint_genre(_summary())
        assert isinstance(hints, list)
        assert len(hints) >= 1

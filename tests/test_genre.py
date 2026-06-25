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

    def test_medium_tempo_pop_rock(self):
        hints = hint_genre(_summary(tempo_bpm=120))
        assert "pop/rock" in hints

    def test_medium_tempo_ambient(self):
        hints = hint_genre(_summary(tempo_bpm=80))
        assert "ambient/chill" in hints

    def test_bass_heavy(self):
        hints = hint_genre(_summary(spectral_centroid_mean=1000))
        assert "bass-heavy/dark" in hints

    def test_high_zcr_percussive(self):
        hints = hint_genre(_summary(zero_crossing_rate_mean=0.20))
        assert "percussive/noisy" in hints

    def test_low_zcr_tonal(self):
        hints = hint_genre(_summary(zero_crossing_rate_mean=0.01))
        assert "tonal/sustained" in hints

    def test_high_onset_density(self):
        # >8 onsets/sec → rhythmically-dense
        hints = hint_genre(_summary(onset_count=300, duration_s=30.0))
        assert "rhythmically-dense" in hints

    def test_low_onset_density(self):
        # <1 onset/sec → sparse/atmospheric
        hints = hint_genre(_summary(onset_count=5, duration_s=30.0))
        assert "sparse/atmospheric" in hints

    def test_zero_duration_no_crash(self):
        """hint_genre must not raise ZeroDivisionError for zero duration."""
        # duration_s=0 is guarded by max(duration_s, 0.1) in the source
        hints = hint_genre(_summary(duration_s=0.0, onset_count=0))
        assert isinstance(hints, list)

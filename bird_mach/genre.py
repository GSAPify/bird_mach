"""Lightweight genre hinting based on audio feature statistics."""

from __future__ import annotations

from bird_mach.analysis import AnalysisSummary


def hint_genre(summary: AnalysisSummary) -> list[str]:
    """Return a list of possible genre hints based on feature values.

    This is a heuristic-based approach — not a trained classifier.
    Useful for suggesting visualization presets to users.
    """
    hints: list[str] = []

    if summary.tempo_bpm >= 140:
        hints.append("electronic/dance")
    elif summary.tempo_bpm >= 100:
        hints.append("pop/rock")
    elif summary.tempo_bpm >= 60:
        hints.append("ambient/chill")
    else:
        hints.append("drone/experimental")

    if summary.spectral_centroid_mean > 4000:
        hints.append("bright/treble-heavy")
    elif summary.spectral_centroid_mean < 1500:
        hints.append("bass-heavy/dark")

    if summary.zero_crossing_rate_mean > 0.15:
        hints.append("percussive/noisy")
    elif summary.zero_crossing_rate_mean < 0.03:
        hints.append("tonal/sustained")

    if summary.onset_count / max(summary.duration_s, 0.1) > 8:
        hints.append("rhythmically-dense")
    elif summary.onset_count / max(summary.duration_s, 0.1) < 1:
        hints.append("sparse/atmospheric")

    return hints

"""Screen reader friendly descriptions for visualizations."""
from __future__ import annotations

def describe_waveform(rms: float, peak: float, duration_s: float) -> str:
    loudness = "loud" if rms > 0.3 else "moderate" if rms > 0.1 else "quiet"
    clip = " with clipping" if peak > 0.99 else ""
    return f"A {loudness} audio waveform lasting {duration_s:.1f} seconds{clip}."

def describe_spectrum(bands: dict[str, float]) -> str:
    dominant = max(bands, key=bands.get) if bands else "unknown"
    return f"Frequency spectrum dominated by {dominant.replace('_', ' ')} frequencies."

def describe_tempo(bpm: float) -> str:
    if bpm < 60:
        feel = "very slow, ambient"
    elif bpm < 100:
        feel = "moderate, relaxed"
    elif bpm < 140:
        feel = "upbeat, energetic"
    else:
        feel = "fast, driving"
    return f"Tempo is {bpm:.0f} BPM — {feel}."

def describe_key(key: str, mode: str) -> str:
    mood = "bright and happy" if mode == "major" else "dark and contemplative"
    return f"Musical key is {key} {mode}, which often sounds {mood}."

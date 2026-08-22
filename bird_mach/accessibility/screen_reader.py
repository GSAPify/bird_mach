"""Screen reader friendly descriptions for visualizations."""
from __future__ import annotations
import math

def describe_waveform(rms: float, peak: float, duration_s: float) -> str:
    loudness = "loud" if rms > 0.3 else "moderate" if rms > 0.1 else "quiet"
    clip = " with clipping" if peak > 0.99 else ""
    return f"A {loudness} audio waveform lasting {duration_s:.1f} seconds{clip}."

def describe_spectrum(bands: dict[str, float]) -> str:
    # A band with a None value would make max() raise on the comparison.
    usable = {k: v for k, v in bands.items() if isinstance(v, (int, float))}
    dominant = max(usable, key=usable.get) if usable else "unknown"
    return f"Frequency spectrum dominated by {dominant.replace('_', ' ')} frequencies."

def describe_tempo(bpm: float) -> str:
    if not math.isfinite(bpm) or bpm < 0:
        return "Tempo is unknown."
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
    normalized = (mode or "").strip().lower()
    if normalized == "major":
        mood = "bright and happy"
    elif normalized == "minor":
        mood = "dark and contemplative"
    else:
        return f"Musical key is {key} {mode}."
    return f"Musical key is {key} {mode}, which often sounds {mood}."

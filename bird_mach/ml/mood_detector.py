"""Audio mood detection from acoustic features."""
from __future__ import annotations

MOOD_RULES = {
    "happy": {"tempo_min": 110, "mode": "major", "energy_min": 0.15},
    "sad": {"tempo_max": 100, "mode": "minor", "energy_max": 0.12},
    "energetic": {"tempo_min": 130, "energy_min": 0.25},
    "calm": {"tempo_max": 90, "energy_max": 0.1},
    "aggressive": {"tempo_min": 140, "energy_min": 0.3, "zcr_min": 0.1},
}

def detect_mood(tempo: float, energy: float, zcr: float = 0.0, mode: str = "major") -> list[dict]:
    matches = []
    for mood, rules in MOOD_RULES.items():
        score = 0.0
        checks = 0
        if "tempo_min" in rules:
            checks += 1
            if tempo >= rules["tempo_min"]: score += 1
        if "tempo_max" in rules:
            checks += 1
            if tempo <= rules["tempo_max"]: score += 1
        if "energy_min" in rules:
            checks += 1
            if energy >= rules["energy_min"]: score += 1
        if "energy_max" in rules:
            checks += 1
            if energy <= rules["energy_max"]: score += 1
        if "mode" in rules:
            checks += 1
            if mode == rules["mode"]: score += 1
        if "zcr_min" in rules:
            checks += 1
            if zcr >= rules["zcr_min"]: score += 1
        if checks > 0:
            confidence = score / checks
            if confidence > 0.5:
                matches.append({"mood": mood, "confidence": round(confidence, 2)})
    matches.sort(key=lambda m: -m["confidence"])
    return matches

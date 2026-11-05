"""Audio mood detection from acoustic features."""
from __future__ import annotations

MOOD_RULES = {
    "happy": {"tempo_min": 110, "mode": "major", "energy_min": 0.15},
    "sad": {"tempo_max": 100, "mode": "minor", "energy_max": 0.12},
    "energetic": {"tempo_min": 130, "energy_min": 0.25},
    "calm": {"tempo_max": 90, "energy_max": 0.1},
    "aggressive": {"tempo_min": 140, "energy_min": 0.3, "zcr_min": 0.1},
}

# rule key -> (feature name, comparison)
RULE_CHECKS = {
    "tempo_min": ("tempo", lambda value, bound: value >= bound),
    "tempo_max": ("tempo", lambda value, bound: value <= bound),
    "energy_min": ("energy", lambda value, bound: value >= bound),
    "energy_max": ("energy", lambda value, bound: value <= bound),
    "mode": ("mode", lambda value, bound: value == bound),
    "zcr_min": ("zcr", lambda value, bound: value >= bound),
}

def detect_mood(tempo: float, energy: float, zcr: float = 0.0, mode: str = "major") -> list[dict]:
    features = {"tempo": tempo, "energy": energy, "zcr": zcr, "mode": mode}
    matches = []
    for mood, rules in MOOD_RULES.items():
        results = [
            compare(features[feature], rules[key])
            for key, (feature, compare) in RULE_CHECKS.items()
            if key in rules
        ]
        if results:
            confidence = sum(results) / len(results)
            if confidence >= 0.5:
                matches.append({"mood": mood, "confidence": round(confidence, 2)})
    matches.sort(key=lambda m: -m["confidence"])
    return matches

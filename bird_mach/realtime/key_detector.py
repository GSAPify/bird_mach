"""Musical key detection from chroma features."""
from __future__ import annotations
import numpy as np

KEY_PROFILES = {
    "major": [6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88],
    "minor": [6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17],
}

class KeyDetector:
    """Detect musical key using Krumhansl-Schmuckler algorithm."""
    def detect(self, chroma: np.ndarray) -> dict:
        if chroma.ndim == 2:
            chroma = np.mean(chroma, axis=1)
        chroma = chroma[:12]
        best_key, best_corr, best_mode = "C", -1.0, "major"
        notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        for mode, profile in KEY_PROFILES.items():
            prof = np.array(profile)
            for i in range(12):
                rolled = np.roll(chroma, -i)
                corr = float(np.corrcoef(rolled, prof)[0, 1])
                if corr > best_corr:
                    best_corr, best_key, best_mode = corr, notes[i], mode
        return {"key": best_key, "mode": best_mode, "confidence": round(best_corr, 3)}

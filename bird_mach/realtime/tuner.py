"""Real-time chromatic tuner."""
from __future__ import annotations
import numpy as np

NOTE_NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

class ChromaticTuner:
    """Detect the closest musical note and cents deviation."""
    def __init__(self, a4_hz: float = 440.0):
        self._a4 = a4_hz

    def tune(self, freq_hz: float) -> dict:
        if freq_hz <= 0:
            return {"note": "—", "octave": 0, "cents": 0.0, "freq": 0.0}
        semitones = 12 * np.log2(freq_hz / self._a4)
        midi = round(semitones) + 69
        note = NOTE_NAMES[midi % 12]
        octave = (midi // 12) - 1
        cents = (semitones - round(semitones)) * 100
        return {"note": note, "octave": octave, "cents": round(cents, 1), "freq": round(freq_hz, 1)}

# Pitch Detection

Mach uses librosa's pYIN algorithm for robust fundamental frequency estimation.

## Usage

```python
from bird_mach.pitch import estimate_pitch, hz_to_note

result = estimate_pitch(y, sr=22050)
print(f"Median pitch: {result.median_hz:.1f} Hz ({hz_to_note(result.median_hz)})")
print(f"Voicing confidence: {result.confidence:.0%}")
```

## PitchResult Fields

| Field | Type | Description |
|-------|------|-------------|
| `f0` | ndarray | Per-frame fundamental frequency (Hz) |
| `voiced_flag` | ndarray | Boolean mask of voiced frames |
| `times_s` | ndarray | Frame timestamps |
| `median_hz` | float | Median frequency of voiced frames |
| `confidence` | float | Fraction of frames detected as voiced |

## Notes

- Default frequency range: C2 (65 Hz) to C7 (2093 Hz)
- Unvoiced frames have f0 = 0.0
- Works best with monophonic audio (single voice/instrument)

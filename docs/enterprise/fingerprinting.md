# Audio Fingerprinting

## Algorithms
- **Chromaprint**: Hash-based fingerprinting for quick similarity
- **Constellation**: Shazam-inspired peak-pair fingerprinting

## Usage
```python
from bird_mach.fingerprint.chromaprint import AudioFingerprinter
fp = AudioFingerprinter()
hash = fp.fingerprint(audio_array)
```

## Matching
```python
from bird_mach.fingerprint.matcher import FingerprintDB
db = FingerprintDB()
db.insert("track1", hashes)
matches = db.search(query_hashes)
```

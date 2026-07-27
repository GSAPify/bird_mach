"""Tests for chromaprint fingerprinting."""
import numpy as np
from bird_mach.fingerprint.chromaprint import AudioFingerprinter

def _two_tone_reference(sr: int, duration: float = 3.0, seed: int = 7) -> np.ndarray:
    """A 3-second two-tone reference signal with a noise floor and envelope,
    representative of a real recording rather than a pure stationary tone."""
    n = int(sr * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    rng = np.random.default_rng(seed)
    envelope = 0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t)
    tones = 0.5 * np.sin(2 * np.pi * 440.3 * t) + 0.3 * np.sin(2 * np.pi * 881.7 * t)
    noise_floor = 0.02 * rng.standard_normal(n)
    return (envelope * tones + noise_floor).astype(np.float32)

class TestAudioFingerprinter:
    def test_fingerprint_returns_bitstring(self):
        fp = AudioFingerprinter(sr=22050)
        y = np.random.randn(22050).astype(np.float32)
        result = fp.fingerprint(y)
        assert isinstance(result, str)
        assert result and set(result) <= {"0", "1"}

    def test_same_audio_same_fingerprint(self):
        fp = AudioFingerprinter()
        y = np.random.default_rng(42).standard_normal(22050).astype(np.float32)
        assert fp.fingerprint(y) == fp.fingerprint(y)

    def test_empty_audio(self):
        fp = AudioFingerprinter()
        assert fp.fingerprint(np.array([], dtype=np.float32)) == ""

    def test_similarity_identical(self):
        fp = AudioFingerprinter()
        h = "1010" * 16
        assert fp.similarity(h, h) == 1.0

    def test_fingerprint_preserves_locality_under_perturbation(self):
        """Regression test for the chromaprint bug: fingerprint() used to return
        sha256(bitstring).hexdigest(), which destroys the locality-preserving
        structure of the underlying bitstring -- a single flipped input bit
        randomizes the whole hash, collapsing similarity() to noise for any
        near-duplicate audio. fingerprint() must return the raw bitstring so
        similarity() behaves as a graded, normalized Hamming similarity:
        near-duplicates score high, unrelated audio stays low.
        """
        sr = 22050
        fp = AudioFingerprinter(sr=sr)
        rng = np.random.default_rng(7)

        ref = _two_tone_reference(sr)
        base = fp.fingerprint(ref)

        gain = (ref * 1.005).astype(np.float32)
        shifted = np.roll(ref, 1).astype(np.float32)
        trimmed = ref[int(0.02 * sr):].astype(np.float32)  # 20ms trimmed from start
        noisy = (ref + rng.normal(0, 0.02, size=ref.shape)).astype(np.float32)
        unrelated = rng.standard_normal(len(ref)).astype(np.float32)

        gain_sim = fp.similarity(base, fp.fingerprint(gain))
        shift_sim = fp.similarity(base, fp.fingerprint(shifted))
        trim_sim = fp.similarity(base, fp.fingerprint(trimmed))
        noise_sim = fp.similarity(base, fp.fingerprint(noisy))
        unrelated_sim = fp.similarity(base, fp.fingerprint(unrelated))

        # Measured with this exact setup: gain=1.0, shift=0.977, trim=0.908,
        # noise=0.968, unrelated=0.525. Assert with margin so the test isn't
        # brittle to platform-specific floating point rounding in the FFT.
        assert gain_sim >= 0.95, gain_sim
        assert shift_sim >= 0.9, shift_sim
        assert trim_sim >= 0.85, trim_sim
        assert noise_sim >= 0.9, noise_sim

        # Unrelated audio must land well below every perturbation case --
        # this is the graded-similarity property the sha256 digest destroyed.
        assert unrelated_sim <= 0.65, unrelated_sim
        assert unrelated_sim < trim_sim - 0.2

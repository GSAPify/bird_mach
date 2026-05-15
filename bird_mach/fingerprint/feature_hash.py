"""Feature-based audio hashing for near-duplicate detection."""
from __future__ import annotations
import numpy as np

def feature_hash(mfcc: np.ndarray, n_bits: int = 128) -> str:
    """Create a locality-sensitive hash from MFCC features.

    The bitstring is returned directly: digesting it would destroy the
    locality that :func:`hamming_distance` relies on, since near-identical
    inputs would produce unrelated digests.
    """
    if mfcc.ndim == 2:
        means = np.mean(mfcc, axis=1)
    else:
        means = mfcc
    if means.size == 0:
        return "0" * n_bits
    median = np.median(means)
    bits = "".join("1" if v > median else "0" for v in means[:n_bits])
    return bits.ljust(n_bits, "0")

def hamming_distance(h1: str, h2: str) -> int:
    if len(h1) != len(h2):
        return max(len(h1), len(h2))
    return sum(a != b for a, b in zip(h1, h2))

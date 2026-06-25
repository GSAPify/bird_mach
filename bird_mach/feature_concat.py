"""Concatenate multiple per-frame features into a single matrix."""

from __future__ import annotations

import numpy as np


def concat_features(*arrays: np.ndarray, align: str = "min") -> np.ndarray:
    """Horizontally stack per-frame feature arrays.

    Each array can be 1-D (single feature per frame) or 2-D (n_features, n_frames).
    All arrays are transposed/reshaped to (n_frames, n_features) and then stacked.

    Args:
        arrays: Variable number of feature arrays.
        align: How to handle different lengths — "min" truncates to shortest.

    Returns:
        Combined feature matrix of shape (n_frames, total_features).
    """
    if not arrays:
        raise ValueError("concat_features requires at least one array")
    _valid_align = {"min"}
    if align not in _valid_align:
        raise ValueError(f"unknown align {align!r}; expected one of {sorted(_valid_align)}")
    normalized = []
    for i, arr in enumerate(arrays):
        if arr.ndim not in (1, 2):
            raise ValueError(
                f"arrays[{i}] has {arr.ndim} dimensions; expected 1 or 2"
            )
        if arr.ndim == 1:
            arr = arr[:, np.newaxis]
        elif arr.shape[0] < arr.shape[1]:
            arr = arr.T
        normalized.append(arr.astype(np.float32, copy=False))

    if align == "min":
        min_len = min(a.shape[0] for a in normalized)
        normalized = [a[:min_len] for a in normalized]

    return np.hstack(normalized)

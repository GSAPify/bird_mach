"""Tests for shared type aliases."""
import numpy as np
import numpy.typing as npt

from bird_mach import types as mach_types

ALIASES = ["AudioArray", "FeatureMatrix", "EmbeddingMatrix", "TimeArray", "EnergyArray"]


def test_all_aliases_are_defined():
    for name in ALIASES:
        assert hasattr(mach_types, name), name


def test_aliases_are_float32_ndarrays():
    for name in ALIASES:
        assert getattr(mach_types, name) == npt.NDArray[np.float32]

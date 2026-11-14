"""Tests for shared type aliases."""
import numpy as np
import numpy.typing as npt

from bird_mach import types as mach_types

ALIASES = ["AudioArray", "FeatureMatrix", "EmbeddingMatrix", "TimeArray", "EnergyArray"]


def test_all_aliases_are_defined():
    for name in ALIASES:
        assert hasattr(mach_types, name), name

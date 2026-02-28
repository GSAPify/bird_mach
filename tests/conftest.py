"""Shared fixtures for Mach test suite."""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture()
def sine_wave() -> np.ndarray:
    """Generate a 1-second 440 Hz sine wave at 22050 Hz sample rate."""
    sr = 22050
    t = np.linspace(0, 1.0, sr, endpoint=False)
    return (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)


@pytest.fixture()
def silence() -> np.ndarray:
    """Generate 1 second of silence at 22050 Hz."""
    return np.zeros(22050, dtype=np.float32)


@pytest.fixture()
def white_noise(rng: np.random.Generator) -> np.ndarray:
    """Generate 1 second of white noise at 22050 Hz."""
    return rng.standard_normal(22050).astype(np.float32)


@pytest.fixture()
def rng() -> np.random.Generator:
    """Seeded random generator for reproducible tests."""
    return np.random.default_rng(42)


@pytest.fixture()
def sample_rate() -> int:
    return 22050

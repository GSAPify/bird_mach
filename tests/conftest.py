"""Shared fixtures for Mach test suite."""

from __future__ import annotations

import asyncio
import inspect

import numpy as np
import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register the ``asyncio`` marker used by async test cases.

    The suite has no async plugin (pytest-asyncio/anyio) installed, so the
    marker would otherwise raise ``PytestUnknownMarkWarning``.
    """
    config.addinivalue_line(
        "markers", "asyncio: run an async test function via asyncio.run()"
    )


def pytest_pyfunc_call(pyfuncitem: pytest.Function):
    """Run ``async def`` test functions on a fresh event loop.

    No async plugin is installed, so pytest cannot natively await coroutine
    test functions. This stdlib-only hook drives any coroutine test to
    completion and returns ``True`` to signal it handled the call. For regular
    (synchronous) test functions it returns ``None`` so pytest's default
    machinery runs unchanged.
    """
    test_fn = pyfuncitem.obj
    if not inspect.iscoroutinefunction(test_fn):
        return None
    funcargs = pyfuncitem.funcargs
    kwargs = {name: funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
    asyncio.run(test_fn(**kwargs))
    return True


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

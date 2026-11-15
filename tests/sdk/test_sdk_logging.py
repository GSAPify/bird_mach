"""Tests for SDK debug logging."""
import logging

import pytest

from bird_mach.sdk import logging as sdk_logging


@pytest.fixture(autouse=True)
def reset_sdk_logger():
    logger = sdk_logging.SDK_LOGGER
    level, handlers = logger.level, list(logger.handlers)
    logger.handlers = []
    yield
    logger.setLevel(level)
    logger.handlers = handlers


def test_enable_debug_sets_level_and_adds_handler():
    sdk_logging.enable_debug()
    assert sdk_logging.SDK_LOGGER.level == logging.DEBUG
    assert len(sdk_logging.SDK_LOGGER.handlers) == 1


def test_enable_debug_does_not_duplicate_handlers():
    sdk_logging.enable_debug()
    sdk_logging.enable_debug()
    assert len(sdk_logging.SDK_LOGGER.handlers) == 1

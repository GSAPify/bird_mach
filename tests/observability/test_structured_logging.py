"""Tests for structured JSON logging."""
import json
import logging
import sys

import pytest

from bird_mach.observability.structured_logging import JSONFormatter, configure_json_logging


def make_record(msg="hello", level=logging.INFO, **extra):
    record = logging.LogRecord("mach.test", level, __file__, 42, msg, None, None)
    for key, value in extra.items():
        setattr(record, key, value)
    return record


@pytest.fixture
def restore_root_logger():
    root = logging.getLogger()
    handlers, level = list(root.handlers), root.level
    yield
    root.handlers = handlers
    root.setLevel(level)


def test_formats_core_fields():
    data = json.loads(JSONFormatter().format(make_record()))
    assert data["level"] == "info"
    assert data["logger"] == "mach.test"
    assert data["message"] == "hello"
    assert data["line"] == 42


def test_level_is_lowercase():
    data = json.loads(JSONFormatter().format(make_record(level=logging.WARNING)))
    assert data["level"] == "warning"


def test_timestamp_is_utc_with_z_suffix():
    data = json.loads(JSONFormatter().format(make_record()))
    assert data["timestamp"].endswith("Z")
    assert "+00:00" not in data["timestamp"]


def test_message_args_are_interpolated():
    record = logging.LogRecord("n", logging.INFO, __file__, 1, "x=%d", (5,), None)
    assert json.loads(JSONFormatter().format(record))["message"] == "x=5"

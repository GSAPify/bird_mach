"""Tests for bird_mach.logging_config."""

import logging

import pytest

from bird_mach.logging_config import setup_logging


class TestSetupLogging:
    def test_unknown_level_raises(self):
        with pytest.raises(ValueError, match="Unknown log level"):
            setup_logging(level="DEBG")

    def test_valid_level_does_not_raise(self):
        # Should not raise for any of the standard levels
        for lvl in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            setup_logging(level=lvl)

    def test_case_insensitive(self):
        setup_logging(level="debug")
        assert logging.getLogger().level == logging.DEBUG

    def test_json_format_accepted(self):
        setup_logging(level="INFO", json_format=True)

    def test_uvicorn_access_silenced(self):
        setup_logging(level="DEBUG")
        assert logging.getLogger("uvicorn.access").level == logging.WARNING

    def test_numba_silenced(self):
        setup_logging(level="DEBUG")
        assert logging.getLogger("numba").level == logging.WARNING

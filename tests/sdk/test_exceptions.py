"""Tests for SDK exceptions."""
import pytest
from bird_mach.sdk.exceptions import (
    MachSDKError, AuthenticationError, RateLimitError, AnalysisError, NotFoundError,
)

class TestExceptions:
    def test_hierarchy(self):
        assert issubclass(AuthenticationError, MachSDKError)
        assert issubclass(RateLimitError, MachSDKError)
        assert issubclass(NotFoundError, MachSDKError)

    def test_rate_limit(self):
        err = RateLimitError(retry_after_s=30.0)
        assert err.retry_after_s == 30.0
        assert "30.0" in str(err)

    def test_analysis_error(self):
        err = AnalysisError("audio-1", "corrupt file")
        assert err.audio_id == "audio-1"
        assert "corrupt" in str(err)

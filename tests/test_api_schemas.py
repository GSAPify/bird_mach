"""Tests for bird_mach.api.schemas."""

from bird_mach.api.schemas import (
    AnalysisRequest,
    AnalysisSummaryResponse,
    HealthResponse,
    ErrorResponse,
)


class TestHealthResponse:
    def test_defaults(self):
        r = HealthResponse(version="0.4.0")
        assert r.status == "ok"
        assert r.app == "Mach"


class TestAnalysisRequest:
    def test_defaults(self):
        req = AnalysisRequest()
        assert req.sr == 22050
        assert req.stride == 2
        assert req.color_by == "time"
        assert req.dimensions == "3d"

    def test_custom_values(self):
        req = AnalysisRequest(sr=44100, stride=5, color_by="energy")
        assert req.sr == 44100


class TestErrorResponse:
    def test_error_message(self):
        r = ErrorResponse(error="bad request", detail="file too large")
        assert r.error == "bad request"

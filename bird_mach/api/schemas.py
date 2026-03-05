"""Pydantic schemas for the Mach REST API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    app: str = "Mach"
    version: str


class AnalysisRequest(BaseModel):
    sr: int = Field(22050, ge=8000, le=48000, description="Target sample rate")
    stride: int = Field(2, ge=1, le=20)
    n_neighbors: int = Field(15, ge=5, le=200)
    min_dist: float = Field(0.1, ge=0.0, le=1.0)
    color_by: str = Field("time", pattern="^(time|energy|flatness)$")
    dimensions: str = Field("3d", pattern="^(2d|3d)$")
    colorscale: str = "Turbo"


class AnalysisSummaryResponse(BaseModel):
    duration_s: float
    sample_rate: int
    tempo_bpm: float
    onset_count: int
    rms_mean: float
    rms_max: float
    spectral_centroid_mean: float
    spectral_bandwidth_mean: float
    zero_crossing_rate_mean: float
    tags: list[str]


class CompareResponse(BaseModel):
    file_a: str
    file_b: str
    diffs: dict[str, dict[str, float]]


class ErrorResponse(BaseModel):
    error: str
    detail: str = ""

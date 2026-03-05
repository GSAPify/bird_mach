"""API v1 routes for programmatic access to Mach analysis."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import librosa
from fastapi import APIRouter, File, UploadFile

from bird_mach.analysis import summarize
from bird_mach.api.schemas import AnalysisSummaryResponse, ErrorResponse, HealthResponse
from bird_mach.constants import APP_NAME, APP_VERSION

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["api"])


@router.get("/health", response_model=HealthResponse)
async def api_health():
    return HealthResponse(version=APP_VERSION)


@router.post(
    "/analyze",
    response_model=AnalysisSummaryResponse,
    responses={400: {"model": ErrorResponse}},
)
async def api_analyze(
    file: UploadFile = File(...),
    sr: int = 22050,
):
    """Analyze an uploaded audio file and return a JSON summary."""
    logger.info("API analyze: %s", file.filename)
    contents = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(contents)
        tmp.flush()
        y, actual_sr = librosa.load(tmp.name, sr=sr, mono=True)

    summary = summarize(y, sr=actual_sr)
    return AnalysisSummaryResponse(
        duration_s=summary.duration_s,
        sample_rate=summary.sample_rate,
        tempo_bpm=summary.tempo_bpm,
        onset_count=summary.onset_count,
        rms_mean=summary.rms_mean,
        rms_max=summary.rms_max,
        spectral_centroid_mean=summary.spectral_centroid_mean,
        spectral_bandwidth_mean=summary.spectral_bandwidth_mean,
        zero_crossing_rate_mean=summary.zero_crossing_rate_mean,
        tags=summary.tags,
    )

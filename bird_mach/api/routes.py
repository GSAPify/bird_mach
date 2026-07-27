"""API v1 routes for programmatic access to Mach analysis."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import librosa
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from bird_mach.analysis import summarize
from bird_mach.api.schemas import AnalysisSummaryResponse, ErrorResponse, HealthResponse
from bird_mach.auth.models import User
from bird_mach.billing.quota import enforce_analysis_quota
from bird_mach.config import AppConfig
from bird_mach.constants import APP_NAME, APP_VERSION

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["api"])

CHUNK_BYTES = 1 << 20


async def read_capped(file: UploadFile) -> bytes:
    """Read an upload in chunks, aborting with 413 once the size cap is passed.

    Avoids materialising an unbounded body in memory: the read stops at the
    first chunk that crosses ``MAX_UPLOAD_MB`` instead of buffering the rest.
    """
    limit = AppConfig.from_env().max_upload_mb * 1024 * 1024
    chunks: list[bytes] = []
    total = 0
    while chunk := await file.read(CHUNK_BYTES):
        total += len(chunk)
        if total > limit:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Audio upload exceeds the {limit // (1024 * 1024)} MB limit.",
            )
        chunks.append(chunk)
    return b"".join(chunks)


def analyze_bytes(contents: bytes, sr: int = 22050) -> AnalysisSummaryResponse:
    """Decode audio bytes and return the analysis summary.

    Shared by the anonymous endpoint and the authenticated/metered routes so
    the load-and-summarize logic lives in exactly one place.
    """
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


@router.get("/health", response_model=HealthResponse)
async def api_health():
    return HealthResponse(version=APP_VERSION)


@router.post(
    "/analyze",
    response_model=AnalysisSummaryResponse,
    responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}},
)
async def api_analyze(
    file: UploadFile = File(...),
    sr: int = 22050,
    user: User = Depends(enforce_analysis_quota),
):
    """Analyze an uploaded audio file and return a JSON summary.

    Metered: counts against the caller's free-tier daily quota. Identical
    gating to ``/api/v1/analyze/metered``; kept as a distinct path because it
    is the documented public API surface.
    """
    logger.info("API analyze: %s (user=%s)", file.filename, user.id)
    return analyze_bytes(await read_capped(file), sr)

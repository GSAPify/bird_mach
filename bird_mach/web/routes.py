"""HTML routes for the Mach web UI.

Lives in its own module so ``bird_mach.webapp`` stays a thin app factory
that wires middleware, the JSON API router, and this UI router together.
"""

from __future__ import annotations

import html
import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bird_mach.config import AppConfig
from bird_mach.constants import SUPPORTED_AUDIO_EXTENSIONS
from bird_mach.embedding import (
    DEFAULT_AUDIO_FEATURE_CONFIG,
    DEFAULT_UMAP_CONFIG,
    AudioFeatureConfig,
    ColorBy,
    UmapConfig,
    build_2d_figure,
    build_energy_figure,
    build_mel_spectrogram_figure,
    build_multiview_figure,
    build_singleview_figure,
    build_waveform_figure,
    compute_umap_2d,
    compute_umap_3d,
    extract_log_mel_frames,
    load_audio_mono_from_path,
    stride_downsample,
)
from bird_mach.web.audio_fetch import fetch_audio_from_url

logger = logging.getLogger(__name__)

WEB_DIR = Path(__file__).resolve().parent
templates_dir = WEB_DIR / "templates"
static_dir = WEB_DIR / "static"

templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


def current_config() -> AppConfig:
    """Resolve request-time configuration so tests and deploy env stay aligned."""
    return AppConfig.from_env()


def supported_formats_label() -> str:
    return ", ".join(ext.lstrip(".") for ext in sorted(SUPPORTED_AUDIO_EXTENSIONS))


def upload_limit_bytes(cfg: AppConfig) -> int:
    return cfg.max_upload_mb * 1024 * 1024


def audio_extension_allowed(filename: str) -> bool:
    return Path(filename).suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS


def visualization_error(message: str, status_code: int = 400) -> HTMLResponse:
    return HTMLResponse(html.escape(message), status_code=status_code)


def upload_page_context(request: Request) -> dict:
    cfg = current_config()
    return {
        "request": request,
        "max_upload_mb": cfg.max_upload_mb,
        "supported_formats": supported_formats_label(),
    }


def normalize_color_by(value: str) -> ColorBy:
    """Coerce free-form form input to the supported color-by values."""
    if value == "energy":
        return "energy"
    return "time"


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", upload_page_context(request))


@router.get("/live", response_class=HTMLResponse)
def live(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "live.html")


@router.post("/visualize", response_class=HTMLResponse)
async def visualize(
    request: Request,
    audio: UploadFile = File(None),
    audio_url: str = Form(""),
    color_by: str = Form("time"),
    colorscale: str = Form("Turbo"),
    dimensions: str = Form("3d"),
    stride: int = Form(2),
    n_neighbors: int = Form(DEFAULT_UMAP_CONFIG.n_neighbors),
    min_dist: float = Form(DEFAULT_UMAP_CONFIG.min_dist),
    multi_view: bool = Form(False),
    connect: bool = Form(False),
) -> HTMLResponse:
    raw: bytes = b""
    filename = "audio"

    if audio and audio.filename:
        raw = await audio.read()
        filename = audio.filename
    elif audio_url.strip():
        try:
            raw, filename = fetch_audio_from_url(audio_url.strip())
        except Exception as e:
            logger.warning("URL fetch failed: %s", e)
            return visualization_error(f"Failed to fetch audio from URL: {e}")

    if not raw:
        logger.warning("No audio provided (neither file nor URL)")
        return visualization_error("No audio received. Upload a file or provide a URL.")

    if not audio_extension_allowed(filename):
        logger.warning("Unsupported audio extension: %s", filename)
        return visualization_error(
            f"Unsupported audio format. Supported formats: {supported_formats_label()}."
        )

    logger.info("Processing: %s (%d bytes)", filename, len(raw))

    stride = max(1, min(stride, 50))
    n_neighbors = max(2, min(n_neighbors, 200))
    min_dist = max(0.0, min(min_dist, 1.0))

    suffix = Path(filename).suffix or ".wav"

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(raw)
            tmp_path = Path(f.name)

        audio_cfg = AudioFeatureConfig(
            sr=DEFAULT_AUDIO_FEATURE_CONFIG.sr,
            n_fft=DEFAULT_AUDIO_FEATURE_CONFIG.n_fft,
            hop_length=DEFAULT_AUDIO_FEATURE_CONFIG.hop_length,
            n_mels=DEFAULT_AUDIO_FEATURE_CONFIG.n_mels,
            fmin=DEFAULT_AUDIO_FEATURE_CONFIG.fmin,
            fmax=DEFAULT_AUDIO_FEATURE_CONFIG.fmax,
        )
        umap_cfg = UmapConfig(
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            metric=DEFAULT_UMAP_CONFIG.metric,
            random_state=DEFAULT_UMAP_CONFIG.random_state,
        )

        y, sr = load_audio_mono_from_path(tmp_path, sr=audio_cfg.sr)
        X, times_s, energy = extract_log_mel_frames(y, sr, audio_cfg)
        X, times_s, energy = stride_downsample(X, times_s, energy, stride=stride)

        use_2d = dimensions.strip().lower() == "2d"
        chosen_color_by = normalize_color_by(color_by)
        dim_label = "2D" if use_2d else "3D"
        title = f"{filename} \u2014 {dim_label} embedding"
        duration_s = float(y.shape[0]) / float(sr)
        summary = (
            f"duration={duration_s:.2f}s frames={X.shape[0]} stride={stride} "
            f"color_by={chosen_color_by} dim={dim_label} connect={connect}"
        )

        if use_2d:
            emb = compute_umap_2d(X, umap_cfg)
            fig = build_2d_figure(
                emb,
                times_s=times_s,
                energy=energy,
                color_by=chosen_color_by,
                connect=connect,
                title=title,
                colorscale=colorscale,
            )
        else:
            emb = compute_umap_3d(X, umap_cfg)
            if multi_view:
                fig = build_multiview_figure(
                    emb,
                    times_s=times_s,
                    energy=energy,
                    color_by=chosen_color_by,
                    connect=connect,
                    title=title,
                    colorscale=colorscale,
                )
            else:
                fig = build_singleview_figure(
                    emb,
                    times_s=times_s,
                    energy=energy,
                    color_by=chosen_color_by,
                    connect=connect,
                    title=title,
                    colorscale=colorscale,
                )

        embedding_html = fig.to_html(include_plotlyjs=True, full_html=False)
        waveform_html = build_waveform_figure(y, sr, title="Waveform").to_html(
            include_plotlyjs=False, full_html=False
        )
        mel_html = build_mel_spectrogram_figure(
            X, times_s, sr=sr, cfg=audio_cfg, title="Log-mel spectrogram (dB)"
        ).to_html(include_plotlyjs=False, full_html=False)
        energy_html = build_energy_figure(times_s, energy, title="Energy over time").to_html(
            include_plotlyjs=False, full_html=False
        )

        sections = [
            ("3D embedding (UMAP)", embedding_html),
            ("Waveform", waveform_html),
            ("Log-mel spectrogram", mel_html),
            ("Energy", energy_html),
        ]
        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "title": title,
                "summary": summary,
                "sections": sections,
            },
        )
    except Exception as e:
        logger.exception("Visualization failed for %s", filename)
        msg = html.escape(str(e))
        return HTMLResponse(
            f"<pre>Failed to visualize audio:\n{msg}</pre>", status_code=500
        )
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass

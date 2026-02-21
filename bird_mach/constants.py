"""Shared constants for the Mach audio visualization application."""

APP_NAME = "Mach"
APP_VERSION = "0.2.0"
APP_DESCRIPTION = "3D audio visualization using UMAP embeddings — any sound, any source"

MAX_UPLOAD_SIZE_MB = 50
MAX_AUDIO_DURATION_S = 600
MAX_URL_FETCH_BYTES = 50 * 1024 * 1024
URL_FETCH_TIMEOUT_S = 30

SUPPORTED_AUDIO_EXTENSIONS = frozenset({
    ".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma",
})

SUPPORTED_COLORSCALES = (
    "Turbo", "Viridis", "Plasma", "Inferno",
    "Magma", "Cividis", "Hot", "Electric",
)

DEFAULT_PLOT_HEIGHT_MULTIVIEW = 900
DEFAULT_PLOT_HEIGHT_SINGLE = 700
DEFAULT_PLOT_HEIGHT_2D = 600
DEFAULT_WAVEFORM_HEIGHT = 260
DEFAULT_SPECTROGRAM_HEIGHT = 320
DEFAULT_ENERGY_HEIGHT = 240
DEFAULT_BANDS_HEIGHT = 120

LIVE_AUDIO_SOURCES = ("file", "mic", "tab")

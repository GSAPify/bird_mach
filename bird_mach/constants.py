"""Shared constants for the Bird Mach application."""

APP_NAME = "Bird Mach"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "3D bird sound visualization using UMAP embeddings"

MAX_UPLOAD_SIZE_MB = 50
SUPPORTED_AUDIO_EXTENSIONS = frozenset({
    ".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma",
})

DEFAULT_PLOT_HEIGHT_MULTIVIEW = 900
DEFAULT_PLOT_HEIGHT_SINGLE = 700
DEFAULT_WAVEFORM_HEIGHT = 260
DEFAULT_SPECTROGRAM_HEIGHT = 320
DEFAULT_ENERGY_HEIGHT = 240

"""Application constants for Mach."""

APP_NAME = "Mach"
APP_VERSION = "0.5.1"
MAX_AUDIO_DURATION_S = 600
MAX_UPLOAD_SIZE_MB = 50
SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"}
SUPPORTED_FORMATS = SUPPORTED_AUDIO_EXTENSIONS
DEFAULT_SAMPLE_RATE = 22050
DEFAULT_HOP_LENGTH = 512
DEFAULT_N_MELS = 128
DEFAULT_N_FFT = 2048
DEFAULT_FADE_IN_S = 0.01
DEFAULT_FADE_OUT_S = 0.05
# UI theme — paired with #e2e8f0 (slate-200) foreground text in templates.
DEFAULT_DARK_BG = "#0f172a"

SUPPORTED_EXPORT_FORMATS = {"json", "csv", "tsv", "html", "md"}
SUPPORTED_COLORSCALES = {
    "Turbo",
    "Viridis",
    "Plasma",
    "Inferno",
    "Magma",
    "Cividis",
    "Hot",
    "Electric",
}
MAX_COLLAB_PARTICIPANTS = 50
MAX_ANNOTATIONS_PER_ROOM = 500
DEFAULT_SHARE_EXPIRY_HOURS = 168
MAX_EFFECTS_CHAIN_LENGTH = 20

"""audio_transcode domain events."""
from dataclasses import dataclass

@dataclass
class AudioTranscodeCreated:
    id: str
    timestamp: float

@dataclass
class AudioTranscodeUpdated:
    id: str
    changes: dict

"""sdk_docs domain events."""
from dataclasses import dataclass

@dataclass
class SdkDocsCreated:
    id: str
    timestamp: float

@dataclass
class SdkDocsUpdated:
    id: str
    changes: dict

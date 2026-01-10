"""report_generation domain events."""
from dataclasses import dataclass

@dataclass
class ReportGenerationCreated:
    id: str
    timestamp: float

@dataclass
class ReportGenerationUpdated:
    id: str
    changes: dict

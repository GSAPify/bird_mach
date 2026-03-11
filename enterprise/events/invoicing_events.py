"""invoicing domain events."""
from dataclasses import dataclass

@dataclass
class InvoicingCreated:
    id: str
    timestamp: float

@dataclass
class InvoicingUpdated:
    id: str
    changes: dict

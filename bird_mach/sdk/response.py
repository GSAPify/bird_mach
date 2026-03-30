"""Standardized SDK response wrapper."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class SDKResponse:
    success: bool
    data: dict = field(default_factory=dict)
    error: str | None = None
    status_code: int = 200
    request_id: str = ""

    @property
    def is_error(self) -> bool:
        return not self.success or self.status_code >= 400

    def raise_for_status(self) -> None:
        if self.is_error:
            raise RuntimeError(self.error or f"Request failed with status {self.status_code}")

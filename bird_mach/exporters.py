"""Export audio analysis results to various formats."""

from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path
from typing import Any


def to_json(data: dict[str, Any], *, indent: int = 2) -> str:
    """Serialize analysis results to a JSON string."""
    def _default(obj: Any) -> Any:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, Path):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    return json.dumps(data, default=_default, indent=indent)


def save_json(data: dict[str, Any], path: Path) -> Path:
    """Write analysis results to a JSON file."""
    path.write_text(to_json(data), encoding="utf-8")
    return path

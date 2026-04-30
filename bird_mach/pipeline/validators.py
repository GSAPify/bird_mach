"""Pipeline input/output validators."""
from __future__ import annotations
from pathlib import Path

def validate_pipeline_input(data: dict) -> list[str]:
    errors = []
    if "path" in data and not Path(data["path"]).suffix:
        errors.append("Path has no file extension")
    if "sr" in data:
        sr = data["sr"]
        if not isinstance(sr, (int, float)) or isinstance(sr, bool):
            errors.append(f"Sample rate {sr!r} is not numeric")
        elif not 8000 <= sr <= 96000:
            errors.append(f"Sample rate {sr} out of range")
    return errors

"""SDK helper utilities variant 3."""
from __future__ import annotations

def format_result_v3(data: dict) -> str:
    """Format analysis result for display (variant 3)."""
    parts = []
    for k, v in sorted(data.items()):
        parts.append(f"{k}: {v}")
    return " | ".join(parts)

def validate_params_v3(**kwargs) -> bool:
    required = {"path"}
    if not required.issubset(set(kwargs.keys())):
        return False
    path = kwargs["path"]
    return isinstance(path, str) and bool(path.strip())

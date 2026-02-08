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


def features_to_csv(
    times_s: Any,
    *,
    columns: dict[str, Any],
) -> str:
    """Convert per-frame feature arrays to CSV.

    Args:
        times_s: 1-D array of frame timestamps.
        columns: Mapping of column_name -> 1-D array of per-frame values.

    Returns:
        CSV string with header row.
    """
    import numpy as np

    buf = StringIO()
    writer = csv.writer(buf)
    header = ["time_s", *columns.keys()]
    writer.writerow(header)

    times = np.asarray(times_s)
    arrays = {k: np.asarray(v) for k, v in columns.items()}
    n_frames = len(times)

    for i in range(n_frames):
        row = [f"{times[i]:.4f}"]
        for arr in arrays.values():
            row.append(f"{arr[i]:.6f}" if i < len(arr) else "")
        writer.writerow(row)

    return buf.getvalue()


def save_csv(content: str, path: Path) -> Path:
    """Write CSV content to a file."""
    path.write_text(content, encoding="utf-8")
    return path


def summary_to_html(summary_dict: dict[str, Any], *, title: str = "Analysis Report") -> str:
    """Render an analysis summary dict as a standalone HTML report."""
    rows = "".join(
        f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>"
        for k, v in summary_dict.items()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #0f172a; color: #e2e8f0; }}
h1 {{ color: #38bdf8; }}
table {{ border-collapse: collapse; width: 100%; max-width: 600px; }}
td {{ padding: 0.5rem 1rem; border-bottom: 1px solid #334155; }}
td:first-child {{ color: #94a3b8; }}
</style>
</head>
<body>
<h1>{title}</h1>
<table>{rows}</table>
</body>
</html>"""

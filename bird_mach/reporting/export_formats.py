"""Export analysis data in various formats."""
from __future__ import annotations
import json
import csv
from io import StringIO

def to_json_lines(records: list[dict]) -> str:
    return "\n".join(json.dumps(r, default=str) for r in records)

def to_csv_string(records: list[dict]) -> str:
    if not records:
        return ""
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
    return buf.getvalue()

def to_tsv_string(records: list[dict]) -> str:
    if not records:
        return ""
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=records[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(records)
    return buf.getvalue()

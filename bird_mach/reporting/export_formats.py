"""Export analysis data in various formats."""
from __future__ import annotations
import json
import csv
from io import StringIO

def to_json_lines(records: list[dict]) -> str:
    return "\n".join(json.dumps(r, default=str) for r in records)

def _all_fieldnames(records: list[dict]) -> list[str]:
    """Union of keys across records, preserving first-seen order.

    Using only the first record's keys makes DictWriter raise as soon as a
    later row carries an extra field.
    """
    return list(dict.fromkeys(k for r in records for k in r))

def to_csv_string(records: list[dict]) -> str:
    if not records:
        return ""
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=_all_fieldnames(records))
    writer.writeheader()
    writer.writerows(records)
    return buf.getvalue()

def to_tsv_string(records: list[dict]) -> str:
    if not records:
        return ""
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=_all_fieldnames(records), delimiter="\t")
    writer.writeheader()
    writer.writerows(records)
    return buf.getvalue()

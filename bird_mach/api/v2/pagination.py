"""Cursor-based and offset pagination utilities."""
from __future__ import annotations
from dataclasses import dataclass
import base64
import json

@dataclass
class Page:
    items: list
    total: int
    has_next: bool
    has_prev: bool
    cursor: str | None = None

def paginate_offset(items: list, offset: int = 0, limit: int = 20) -> Page:
    if offset < 0 or limit < 1:
        raise ValueError("offset must be >= 0 and limit must be >= 1")
    total = len(items)
    page_items = items[offset:offset + limit]
    return Page(
        items=page_items, total=total,
        has_next=offset + limit < total,
        has_prev=offset > 0,
    )

def encode_cursor(data: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())

def paginate_cursor(items: list, after: str | None = None, limit: int = 20) -> Page:
    start = 0
    if after:
        cursor_data = decode_cursor(after)
        start = cursor_data.get("offset", 0) + 1
    end = start + limit
    page_items = items[start:end]
    next_cursor = encode_cursor({"offset": end - 1}) if end < len(items) else None
    return Page(
        items=page_items, total=len(items),
        has_next=end < len(items), has_prev=start > 0,
        cursor=next_cursor,
    )

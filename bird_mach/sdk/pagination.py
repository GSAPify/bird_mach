"""SDK-side pagination helpers for consuming paginated API responses."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class PageIterator:
    """Iterate through paginated API results."""
    items: list
    cursor: str | None
    has_more: bool

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

def merge_pages(pages: list[PageIterator]) -> list:
    result = []
    for page in pages:
        result.extend(page.items)
    return result

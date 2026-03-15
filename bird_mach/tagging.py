"""Audio tagging and labeling system."""
from __future__ import annotations
from collections import defaultdict

class TagManager:
    """Manage tags across audio files and projects."""
    def __init__(self):
        self._tags: dict[str, set[str]] = defaultdict(set)
        self._reverse: dict[str, set[str]] = defaultdict(set)

    def tag(self, resource_id: str, tag: str) -> None:
        self._tags[resource_id].add(tag)
        self._reverse[tag].add(resource_id)

    def untag(self, resource_id: str, tag: str) -> None:
        self._tags[resource_id].discard(tag)
        self._reverse[tag].discard(resource_id)

    def get_tags(self, resource_id: str) -> set[str]:
        return self._tags.get(resource_id, set())

    def find_by_tag(self, tag: str) -> set[str]:
        return self._reverse.get(tag, set())

    def popular_tags(self, n: int = 10) -> list[tuple[str, int]]:
        counts = [(tag, len(ids)) for tag, ids in self._reverse.items()]
        counts.sort(key=lambda x: -x[1])
        return counts[:n]

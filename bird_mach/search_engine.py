"""Full-text search across audio metadata and analyses."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass
class SearchResult:
    id: str
    title: str
    score: float
    snippet: str
    resource_type: str

class AudioSearchEngine:
    """Simple in-memory full-text search for audio metadata."""

    def __init__(self):
        self._documents: dict[str, dict] = {}

    def index(self, doc_id: str, title: str, content: str,
              resource_type: str = "audio", metadata: dict | None = None):
        self._documents[doc_id] = {
            "title": title, "content": content.lower(),
            "resource_type": resource_type,
            "metadata": metadata or {},
        }

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        terms = query.lower().split()
        results = []
        for doc_id, doc in self._documents.items():
            text = f"{doc['title']} {doc['content']}".lower()
            score = sum(text.count(term) for term in terms)
            if score > 0:
                snippet = self._extract_snippet(doc["content"], terms[0])
                results.append(SearchResult(
                    id=doc_id, title=doc["title"],
                    score=score, snippet=snippet,
                    resource_type=doc["resource_type"],
                ))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    @staticmethod
    def _extract_snippet(content: str, term: str, context: int = 50) -> str:
        idx = content.find(term)
        if idx == -1:
            return content[:100]
        start = max(0, idx - context)
        end = min(len(content), idx + len(term) + context)
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet

    def remove(self, doc_id: str) -> bool:
        return self._documents.pop(doc_id, None) is not None

    @property
    def document_count(self) -> int:
        return len(self._documents)

"""API versioning helpers."""
from __future__ import annotations

SUPPORTED_VERSIONS = {"v1", "v2"}
DEFAULT_VERSION = "v2"

def parse_version(accept_header: str) -> str:
    if "version=2" in accept_header or "v2" in accept_header:
        return "v2"
    if "version=1" in accept_header or "v1" in accept_header:
        return "v1"
    return DEFAULT_VERSION

def is_deprecated(version: str) -> bool:
    return version == "v1"

def deprecation_header(version: str) -> dict[str, str]:
    if is_deprecated(version):
        return {"Deprecation": "true", "Sunset": "2026-09-01",
                "Link": "</api/v2>; rel="successor-version""}
    return {}

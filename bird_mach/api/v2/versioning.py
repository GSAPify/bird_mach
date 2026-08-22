"""API versioning helpers."""
from __future__ import annotations
import re

SUPPORTED_VERSIONS = {"v1", "v2"}
DEFAULT_VERSION = "v2"

# Match version=2 or a path/token "v2", but not substrings like "v20" or
# "application/vnd.foo" accidentally containing "v1".
_VERSION_RE = re.compile(
    r"(?:(?:^|[;,\s/])\s*version\s*=\s*|[/;,\s]v)([12])(?:[^\d]|$)",
    re.I,
)


def parse_version(accept_header: str) -> str:
    match = _VERSION_RE.search(f" {accept_header}")
    if match:
        return f"v{match.group(1)}"
    return DEFAULT_VERSION

def is_deprecated(version: str) -> bool:
    return version == "v1"

def deprecation_header(version: str) -> dict[str, str]:
    if is_deprecated(version):
        return {"Deprecation": "true", "Sunset": "2026-09-01",
                "Link": '</api/v2>; rel="successor-version"'}
    return {}

"""Helpers for safely pulling remote audio into the visualizer.

Kept separate from the route module so the network/security policy stays
in one easy-to-audit place.
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.request
from email.message import Message
from pathlib import Path
from urllib.parse import unquote, urlparse

from bird_mach.constants import APP_VERSION, SUPPORTED_AUDIO_EXTENSIONS

MAX_REMOTE_BYTES = 50 * 1024 * 1024  # 50 MB
USER_AGENT = f"Mach/{APP_VERSION} (+https://github.com/GSAPify/bird_mach)"
REQUEST_TIMEOUT_S = 30
CONTENT_TYPE_EXTENSIONS = {
    "audio/aac": ".aac",
    "audio/flac": ".flac",
    "audio/mp3": ".mp3",
    "audio/mp4": ".m4a",
    "audio/mpeg": ".mp3",
    "audio/ogg": ".ogg",
    "audio/wav": ".wav",
    "audio/wave": ".wav",
    "audio/x-aac": ".aac",
    "audio/x-flac": ".flac",
    "audio/x-m4a": ".m4a",
    "audio/x-wav": ".wav",
    "application/ogg": ".ogg",
}


def _remote_content_length(headers: object) -> int | None:
    value = headers.get("Content-Length") if hasattr(headers, "get") else None
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _header_content_type(headers: object) -> str:
    raw = headers.get("Content-Type", "") if hasattr(headers, "get") else ""
    return raw.split(";", 1)[0].strip().lower()


def _header_filename(headers: object) -> str:
    raw = headers.get("Content-Disposition", "") if hasattr(headers, "get") else ""
    if not raw:
        return ""
    message = Message()
    message["Content-Disposition"] = raw
    filename = message.get_filename() or ""
    return Path(unquote(filename)).name


def _response_filename(url_path: str, headers: object) -> str:
    header_name = _header_filename(headers)
    path_name = Path(unquote(url_path)).name
    filename = header_name or path_name or "remote_audio"

    suffix = Path(filename).suffix.lower()
    content_type_suffix = CONTENT_TYPE_EXTENSIONS.get(_header_content_type(headers), "")
    if suffix in SUPPORTED_AUDIO_EXTENSIONS:
        return filename
    if content_type_suffix:
        stem = Path(filename).stem or "remote_audio"
        return f"{stem}{content_type_suffix}"
    return filename


def assert_public_url(url: str) -> None:
    """Reject anything that is not an http(s) URL resolving to a global address.

    Blocks SSRF against loopback, RFC1918, link-local (cloud metadata),
    reserved and multicast ranges. Applied to the initial URL and re-applied
    to every redirect target by ``GuardedRedirectHandler``.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are supported")
    host = parsed.hostname
    if not host:
        raise ValueError("URL must include a hostname")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except (socket.gaierror, ValueError) as exc:
        raise ValueError("Could not resolve the URL hostname") from exc
    for info in infos:
        address = ipaddress.ip_address(info[4][0])
        if (
            not address.is_global
            or address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_reserved
            or address.is_multicast
        ):
            raise ValueError("URL resolves to a non-public address")


class GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-run the SSRF check on every redirect hop, not just the first URL."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> urllib.request.Request | None:
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is not None:
            assert_public_url(new_req.full_url)
        return new_req


URL_OPENER = urllib.request.build_opener(GuardedRedirectHandler())


def fetch_audio_from_url(url: str) -> tuple[bytes, str]:
    """Download audio from a public http(s) URL.

    Returns ``(bytes, filename)``. Raises ``ValueError`` for unsupported
    schemes and non-public destinations, and ``urllib.error.URLError``
    (or subclasses) on network failure.
    """
    parsed = urlparse(url)
    assert_public_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with URL_OPENER.open(req, timeout=REQUEST_TIMEOUT_S) as resp:
        content_length = _remote_content_length(resp.headers)
        if content_length is not None and content_length > MAX_REMOTE_BYTES:
            raise ValueError("Remote audio exceeds the 50 MB limit")
        data = resp.read(MAX_REMOTE_BYTES + 1)
        if len(data) > MAX_REMOTE_BYTES:
            raise ValueError("Remote audio exceeds the 50 MB limit")
        filename = _response_filename(parsed.path, resp.headers)
    return data, filename

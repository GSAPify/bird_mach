from __future__ import annotations

import ipaddress
import socket
from email.message import Message

import pytest

from bird_mach.web import audio_fetch

# Hosts used by these tests resolve through this table instead of real DNS.
HOST_IPS = {
    "localhost": "127.0.0.1",
    "internal.example.com": "10.0.0.5",
    "metadata.example.com": "169.254.169.254",
}
DEFAULT_TEST_IP = "93.184.216.34"


@pytest.fixture(autouse=True)
def stub_dns(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_getaddrinfo(host: str, port: int, *args: object, **kwargs: object) -> list[tuple]:
        try:
            ip = str(ipaddress.ip_address(host))
        except ValueError:
            ip = HOST_IPS.get(host, DEFAULT_TEST_IP)
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port))]

    monkeypatch.setattr(audio_fetch.socket, "getaddrinfo", fake_getaddrinfo)


class FakeResponse:
    def __init__(self, body: bytes, headers: dict[str, str] | None = None) -> None:
        self.body = body
        self.headers = headers or {}

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc_info: object) -> None:
        return None

    def read(self, size: int) -> bytes:
        return self.body[:size]


def test_fetch_audio_rejects_large_content_length(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audio_fetch, "MAX_REMOTE_BYTES", 8)

    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"", {"Content-Length": "9"})

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fake_urlopen)

    with pytest.raises(ValueError, match="50 MB limit"):
        audio_fetch.fetch_audio_from_url("https://example.com/audio.wav")


def test_fetch_audio_rejects_body_that_exceeds_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audio_fetch, "MAX_REMOTE_BYTES", 8)

    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"123456789")

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fake_urlopen)

    with pytest.raises(ValueError, match="50 MB limit"):
        audio_fetch.fetch_audio_from_url("https://example.com/audio.wav")


def test_fetch_audio_returns_remote_filename(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"audio")

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fake_urlopen)

    data, filename = audio_fetch.fetch_audio_from_url("https://example.com/path/song.mp3")

    assert data == b"audio"
    assert filename == "song.mp3"


def test_fetch_audio_infers_extension_from_content_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"audio", {"Content-Type": "audio/mpeg; charset=binary"})

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fake_urlopen)

    data, filename = audio_fetch.fetch_audio_from_url("https://cdn.example.com/watch?id=1")

    assert data == b"audio"
    assert filename == "watch.mp3"


def test_fetch_audio_prefers_content_disposition_filename(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(
            b"audio",
            {
                "Content-Disposition": 'attachment; filename="mixdown.wav"',
                "Content-Type": "application/octet-stream",
            },
        )

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fake_urlopen)

    data, filename = audio_fetch.fetch_audio_from_url("https://cdn.example.com/download")

    assert data == b"audio"
    assert filename == "mixdown.wav"


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost:8000/admin",
        "http://127.0.0.1/admin",
        "http://10.0.0.5/internal",
        "http://192.168.1.1/router",
        "http://169.254.169.254/latest/meta-data/",
        "http://[::1]/admin",
    ],
)
def test_fetch_audio_rejects_non_public_destinations(
    url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_open(request: object, timeout: int) -> FakeResponse:
        raise AssertionError("request must not be issued for a non-public destination")

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fail_open)

    with pytest.raises(ValueError, match="non-public address"):
        audio_fetch.fetch_audio_from_url(url)


def test_fetch_audio_allows_public_destination(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"audio")

    monkeypatch.setattr(audio_fetch.URL_OPENER, "open", fake_urlopen)

    data, filename = audio_fetch.fetch_audio_from_url("https://cdn.example.com/track.wav")

    assert data == b"audio"
    assert filename == "track.wav"


def test_redirect_from_public_host_into_internal_range_is_blocked() -> None:
    handler = audio_fetch.GuardedRedirectHandler()
    request = audio_fetch.urllib.request.Request("https://cdn.example.com/track.wav")

    with pytest.raises(ValueError, match="non-public address"):
        handler.redirect_request(
            request, None, 302, "Found", Message(), "http://internal.example.com/secret"
        )

    with pytest.raises(ValueError, match="non-public address"):
        handler.redirect_request(
            request, None, 302, "Found", Message(), "http://metadata.example.com/latest/meta-data/"
        )


def test_redirect_to_public_host_is_allowed() -> None:
    handler = audio_fetch.GuardedRedirectHandler()
    request = audio_fetch.urllib.request.Request("https://cdn.example.com/track.wav")

    redirected = handler.redirect_request(
        request, None, 302, "Found", Message(), "https://media.example.com/track.wav"
    )

    assert redirected is not None
    assert redirected.full_url == "https://media.example.com/track.wav"


def test_guarded_redirect_handler_is_installed_on_the_opener() -> None:
    assert any(
        isinstance(handler, audio_fetch.GuardedRedirectHandler)
        for handler in audio_fetch.URL_OPENER.handlers
    )

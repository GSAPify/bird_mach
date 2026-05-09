from __future__ import annotations

import pytest

from bird_mach.web import audio_fetch


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

    monkeypatch.setattr(audio_fetch.urllib.request, "urlopen", fake_urlopen)

    with pytest.raises(ValueError, match="50 MB limit"):
        audio_fetch.fetch_audio_from_url("https://example.com/audio.wav")


def test_fetch_audio_rejects_body_that_exceeds_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audio_fetch, "MAX_REMOTE_BYTES", 8)

    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"123456789")

    monkeypatch.setattr(audio_fetch.urllib.request, "urlopen", fake_urlopen)

    with pytest.raises(ValueError, match="50 MB limit"):
        audio_fetch.fetch_audio_from_url("https://example.com/audio.wav")


def test_fetch_audio_returns_remote_filename(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: int) -> FakeResponse:
        return FakeResponse(b"audio")

    monkeypatch.setattr(audio_fetch.urllib.request, "urlopen", fake_urlopen)

    data, filename = audio_fetch.fetch_audio_from_url("https://example.com/path/song.mp3")

    assert data == b"audio"
    assert filename == "song.mp3"

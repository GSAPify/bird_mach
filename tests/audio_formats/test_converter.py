"""Tests for FormatConverter."""
import subprocess

import pytest

from bird_mach.audio_formats import converter as converter_mod
from bird_mach.audio_formats.converter import FormatConverter


@pytest.fixture
def calls(monkeypatch):
    recorded = []

    def fake_run(cmd, **kwargs):
        recorded.append((cmd, kwargs))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="info text")

    monkeypatch.setattr(converter_mod.subprocess, "run", fake_run)
    return recorded


@pytest.fixture
def src(tmp_path):
    path = tmp_path / "in.mp3"
    path.write_bytes(b"x")
    return path


def test_convert_missing_source_raises(tmp_path, calls):
    with pytest.raises(FileNotFoundError):
        FormatConverter().convert(tmp_path / "nope.mp3", tmp_path / "out.wav")
    assert calls == []


def test_convert_refuses_to_overwrite_source(src, calls):
    with pytest.raises(ValueError):
        FormatConverter().convert(src, src)
    assert calls == []

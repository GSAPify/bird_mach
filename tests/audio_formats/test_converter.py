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


def test_convert_builds_ffmpeg_command(src, tmp_path, calls):
    dst = tmp_path / "out.wav"
    assert FormatConverter().convert(src, dst) == dst
    cmd, kwargs = calls[0]
    assert cmd == ["ffmpeg", "-i", str(src), "-y", str(dst)]
    assert kwargs["check"] is True and kwargs["timeout"] == 120


def test_convert_adds_sample_rate(src, tmp_path, calls):
    FormatConverter().convert(src, tmp_path / "out.wav", sr=16000)
    cmd = calls[0][0]
    assert cmd[cmd.index("-ar") + 1] == "16000"


def test_convert_rejects_non_positive_sample_rate(src, tmp_path, calls):
    with pytest.raises(ValueError):
        FormatConverter().convert(src, tmp_path / "out.wav", sr=0)
    assert calls == []


def test_to_wav_uses_wav_suffix_and_default_rate(src, calls):
    out = FormatConverter().to_wav(src)
    assert out == src.with_suffix(".wav")
    cmd = calls[0][0]
    assert cmd[cmd.index("-ar") + 1] == "22050"

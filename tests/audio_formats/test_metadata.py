"""Tests for audio metadata extraction."""
import pytest

from bird_mach.audio_formats.metadata import AudioMetadata, extract_metadata


def test_defaults_are_empty():
    meta = AudioMetadata()
    assert meta.title is None and meta.duration_s is None
    assert meta.file_size_bytes == 0


def test_file_size_mb_conversion():
    assert AudioMetadata(file_size_bytes=1024 * 1024).file_size_mb == 1.0


def test_file_size_mb_handles_fractions():
    assert AudioMetadata(file_size_bytes=512 * 1024).file_size_mb == 0.5


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_metadata(tmp_path / "nope.wav")


def test_extracts_size_and_format(tmp_path):
    path = tmp_path / "clip.wav"
    path.write_bytes(b"\0" * 2048)
    meta = extract_metadata(path)
    assert meta.file_size_bytes == 2048
    assert meta.format == "wav"
    assert meta.title is None and meta.sample_rate is None


def test_file_without_extension_has_empty_format(tmp_path):
    path = tmp_path / "clip"
    path.write_bytes(b"x")
    assert extract_metadata(path).format == ""

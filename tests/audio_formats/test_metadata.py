"""Tests for audio metadata extraction."""
import pytest

from bird_mach.audio_formats.metadata import AudioMetadata, extract_metadata


def test_defaults_are_empty():
    meta = AudioMetadata()
    assert meta.title is None and meta.duration_s is None
    assert meta.file_size_bytes == 0

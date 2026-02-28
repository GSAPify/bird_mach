"""Tests for bird_mach.validators."""

from __future__ import annotations

from bird_mach.validators import (
    clamp,
    clamp_int,
    sanitize_url,
    validate_audio_extension,
    validate_file_size,
)


class TestValidateAudioExtension:
    def test_accepts_wav(self):
        assert validate_audio_extension("test.wav") is True

    def test_accepts_mp3(self):
        assert validate_audio_extension("song.MP3") is True

    def test_rejects_txt(self):
        assert validate_audio_extension("notes.txt") is False

    def test_rejects_empty(self):
        assert validate_audio_extension("noext") is False


class TestValidateFileSize:
    def test_within_limit(self):
        assert validate_file_size(1024) is True

    def test_at_limit(self):
        assert validate_file_size(50 * 1024 * 1024) is True

    def test_over_limit(self):
        assert validate_file_size(51 * 1024 * 1024) is False


class TestClamp:
    def test_within_range(self):
        assert clamp(5.0, 0.0, 10.0) == 5.0

    def test_below_range(self):
        assert clamp(-1.0, 0.0, 10.0) == 0.0

    def test_above_range(self):
        assert clamp(15.0, 0.0, 10.0) == 10.0


class TestClampInt:
    def test_clamps_correctly(self):
        assert clamp_int(25, 1, 20) == 20
        assert clamp_int(-5, 1, 20) == 1
        assert clamp_int(10, 1, 20) == 10


class TestSanitizeUrl:
    def test_valid_https(self):
        assert sanitize_url("https://example.com/audio.wav") == "https://example.com/audio.wav"

    def test_valid_http(self):
        assert sanitize_url("http://example.com") == "http://example.com"

    def test_rejects_ftp(self):
        assert sanitize_url("ftp://example.com") is None

    def test_rejects_empty(self):
        assert sanitize_url("") is None
        assert sanitize_url("   ") is None

    def test_strips_whitespace(self):
        assert sanitize_url("  https://example.com  ") == "https://example.com"

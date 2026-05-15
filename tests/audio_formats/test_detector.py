"""Tests for format detection."""
from pathlib import Path
from bird_mach.audio_formats.detector import detect_format, is_supported

class TestDetector:
    def test_wav(self, tmp_path):
        f = tmp_path / "test.wav"
        f.write_bytes(b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 100)
        assert detect_format(f) == "wav"

    def test_riff_without_wave_is_not_audio(self, tmp_path):
        f = tmp_path / "test.avi"
        f.write_bytes(b"RIFF" + b"\x00" * 4 + b"AVI " + b"\x00" * 100)
        assert detect_format(f) is None

    def test_mp3_id3(self, tmp_path):
        f = tmp_path / "test.mp3"
        f.write_bytes(b"ID3" + b"\x00" * 100)
        assert detect_format(f) == "mp3"

    def test_flac(self, tmp_path):
        f = tmp_path / "test.flac"
        f.write_bytes(b"fLaC" + b"\x00" * 100)
        assert detect_format(f) == "flac"

    def test_unknown(self, tmp_path):
        f = tmp_path / "test.bin"
        f.write_bytes(b"\x00" * 100)
        assert detect_format(f) is None

    def test_is_supported(self, tmp_path):
        f = tmp_path / "test.wav"
        f.write_bytes(b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 100)
        assert is_supported(f)

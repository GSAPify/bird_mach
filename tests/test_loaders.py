"""Tests for bird_mach.io.loaders."""

import pytest
from pathlib import Path

from bird_mach.exceptions import AudioLoadError
from bird_mach.io.loaders import load_audio


class TestLoadAudio:
    def test_missing_file_raises(self):
        with pytest.raises(AudioLoadError, match="not found"):
            load_audio(Path("/nonexistent/audio.wav"))

    def test_unsupported_format_raises(self, tmp_path):
        bad_file = tmp_path / "test.xyz"
        bad_file.write_text("not audio")
        with pytest.raises(AudioLoadError, match="Unsupported"):
            load_audio(bad_file)

"""Tests for bird_mach.audio_utils."""

import numpy as np
import pytest
import soundfile as sf

from bird_mach.audio_utils import AudioInfo, normalize_waveform, probe_audio, trim_silence


class TestNormalizeWaveform:
    def test_empty_array_unchanged(self):
        y = np.array([], dtype=np.float32)
        result = normalize_waveform(y)
        assert result.size == 0

    def test_all_zeros_unchanged(self):
        """Sub-threshold peak must not divide-by-zero or alter the signal."""
        y = np.zeros(100, dtype=np.float32)
        result = normalize_waveform(y)
        np.testing.assert_array_equal(result, y)

    def test_sub_threshold_peak_unchanged(self):
        """Peak exactly at the 1e-8 boundary should not be normalized."""
        y = np.full(10, 1e-9, dtype=np.float64)
        result = normalize_waveform(y)
        np.testing.assert_array_equal(result, y)

    def test_peak_scales_to_one(self):
        y = np.array([0.0, 0.5, -2.0, 1.0], dtype=np.float64)
        result = normalize_waveform(y)
        assert abs(np.max(np.abs(result)) - 1.0) < 1e-9

    def test_already_normalized_unchanged(self):
        y = np.array([1.0, -1.0, 0.5], dtype=np.float64)
        result = normalize_waveform(y)
        np.testing.assert_allclose(result, y)

    def test_shape_preserved(self):
        y = np.array([[0.5, -0.5], [0.25, -0.25]], dtype=np.float64)
        result = normalize_waveform(y)
        assert result.shape == y.shape


class TestAudioInfoSizeMb:
    def test_nonexistent_path_returns_zero(self, tmp_path):
        from pathlib import Path

        info = AudioInfo(
            path=tmp_path / "no_such_file.wav",
            duration_s=1.0,
            sample_rate=22050,
            channels=1,
        )
        assert info.size_mb == 0.0

    def test_existing_file_returns_positive(self, tmp_path):
        f = tmp_path / "dummy.wav"
        f.write_bytes(b"\x00" * 1024)  # 1 KiB
        info = AudioInfo(path=f, duration_s=0.1, sample_rate=22050, channels=1)
        expected_mb = 1024 / (1024 * 1024)
        assert abs(info.size_mb - expected_mb) < 1e-9


class TestProbeAudio:
    def test_mono_channel_count(self, tmp_path):
        wav = tmp_path / "mono.wav"
        data = np.zeros(22050, dtype=np.float32)
        sf.write(str(wav), data, 22050)
        info = probe_audio(wav)
        assert info.channels == 1

    def test_stereo_channel_count(self, tmp_path):
        wav = tmp_path / "stereo.wav"
        data = np.zeros((22050, 2), dtype=np.float32)
        sf.write(str(wav), data, 22050)
        info = probe_audio(wav)
        assert info.channels == 2

    def test_sample_rate_passthrough(self, tmp_path):
        wav = tmp_path / "sr.wav"
        data = np.zeros(16000, dtype=np.float32)
        sf.write(str(wav), data, 16000)
        info = probe_audio(wav, sr=8000)
        assert info.sample_rate == 8000  # explicit sr overrides file sr

    def test_sample_rate_from_file(self, tmp_path):
        wav = tmp_path / "sr44.wav"
        data = np.zeros(44100, dtype=np.float32)
        sf.write(str(wav), data, 44100)
        info = probe_audio(wav)
        assert info.sample_rate == 44100


class TestTrimSilence:
    def test_returns_three_tuple(self):
        sr = 22050
        # A short sine burst flanked by silence
        t = np.linspace(0, 0.1, int(sr * 0.1))
        burst = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        silence = np.zeros(sr // 4, dtype=np.float32)
        y = np.concatenate([silence, burst, silence])
        trimmed, start, end = trim_silence(y, sr=sr)
        assert isinstance(trimmed, np.ndarray)
        assert isinstance(start, int)
        assert isinstance(end, int)
        assert start >= 0
        assert end > start

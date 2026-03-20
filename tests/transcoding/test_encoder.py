"""Tests for encoder config."""
from bird_mach.transcoding.encoder import EncoderConfig, Codec, PRESETS

class TestEncoderConfig:
    def test_ffmpeg_args_mp3(self):
        cfg = EncoderConfig(Codec.MP3, bitrate_kbps=192)
        args = cfg.to_ffmpeg_args()
        assert "-c:a" in args
        assert "libmp3lame" in args
        assert "192k" in args

    def test_flac_no_bitrate(self):
        cfg = EncoderConfig(Codec.FLAC)
        args = cfg.to_ffmpeg_args()
        assert "192k" not in " ".join(args)

    def test_presets_exist(self):
        assert "podcast" in PRESETS
        assert "music_high" in PRESETS
        assert PRESETS["podcast"].channels == 1

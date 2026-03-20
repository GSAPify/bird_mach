"""Audio encoder configuration and management."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Codec(Enum):
    PCM = "pcm"
    MP3 = "mp3"
    AAC = "aac"
    FLAC = "flac"
    OGG = "ogg"
    OPUS = "opus"

@dataclass
class EncoderConfig:
    codec: Codec
    bitrate_kbps: int = 128
    sample_rate: int = 44100
    channels: int = 2
    vbr: bool = False
    quality: int = 5

    def to_ffmpeg_args(self) -> list[str]:
        args = ["-ar", str(self.sample_rate), "-ac", str(self.channels)]
        codec_map = {Codec.MP3: "libmp3lame", Codec.AAC: "aac",
                    Codec.FLAC: "flac", Codec.OGG: "libvorbis", Codec.OPUS: "libopus"}
        if self.codec in codec_map:
            args.extend(["-c:a", codec_map[self.codec]])
        if self.codec != Codec.FLAC and self.codec != Codec.PCM:
            if self.vbr:
                args.extend(["-q:a", str(self.quality)])
            else:
                args.extend(["-b:a", f"{self.bitrate_kbps}k"])
        return args

PRESETS = {
    "podcast": EncoderConfig(Codec.MP3, bitrate_kbps=96, sample_rate=44100, channels=1),
    "music_high": EncoderConfig(Codec.FLAC, sample_rate=44100, channels=2),
    "music_lossy": EncoderConfig(Codec.MP3, bitrate_kbps=320, sample_rate=44100, channels=2),
    "voice": EncoderConfig(Codec.OPUS, bitrate_kbps=64, sample_rate=16000, channels=1),
    "streaming": EncoderConfig(Codec.AAC, bitrate_kbps=128, sample_rate=44100, channels=2),
}

#!/usr/bin/env python3
"""CLI tool for running Mach audio analysis on a file.

Usage:
    python scripts/analyze_audio.py path/to/audio.wav
    python scripts/analyze_audio.py path/to/audio.mp3 --output results.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import librosa

from bird_mach.analysis import summarize
from bird_mach.exporters import to_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze an audio file and print a feature summary.",
    )
    parser.add_argument("audio_path", type=Path, help="Path to audio file")
    parser.add_argument("--sr", type=int, default=22050, help="Target sample rate")
    parser.add_argument("--output", "-o", type=Path, help="Save JSON output to file")
    args = parser.parse_args()

    if not args.audio_path.exists():
        print(f"Error: file not found: {args.audio_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {args.audio_path} ...")
    y, sr = librosa.load(str(args.audio_path), sr=args.sr, mono=True)
    print(f"  Loaded {len(y)/sr:.2f}s at {sr} Hz")

    print("Analyzing ...")
    summary = summarize(y, sr=sr)

    result = {
        "file": str(args.audio_path),
        "duration_s": summary.duration_s,
        "sample_rate": summary.sample_rate,
        "tempo_bpm": summary.tempo_bpm,
        "onset_count": summary.onset_count,
        "rms_mean": summary.rms_mean,
        "rms_max": summary.rms_max,
        "spectral_centroid_mean": summary.spectral_centroid_mean,
        "spectral_bandwidth_mean": summary.spectral_bandwidth_mean,
        "zero_crossing_rate_mean": summary.zero_crossing_rate_mean,
        "tags": summary.tags,
    }

    json_str = to_json(result)
    print(json_str)

    if args.output:
        args.output.write_text(json_str, encoding="utf-8")
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()

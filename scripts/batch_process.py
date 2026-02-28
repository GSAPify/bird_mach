#!/usr/bin/env python3
"""Batch-process a directory of audio files and export analysis summaries.

Usage:
    python scripts/batch_process.py ./audio_samples/ --output results/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import librosa

from bird_mach.analysis import summarize
from bird_mach.constants import SUPPORTED_AUDIO_EXTENSIONS
from bird_mach.exporters import save_json


def find_audio_files(directory: Path) -> list[Path]:
    """Recursively find audio files in a directory."""
    files = []
    for ext in SUPPORTED_AUDIO_EXTENSIONS:
        files.extend(directory.rglob(f"*{ext}"))
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-analyze audio files in a directory.",
    )
    parser.add_argument("input_dir", type=Path, help="Directory containing audio files")
    parser.add_argument("--output", "-o", type=Path, default=Path("results"), help="Output directory")
    parser.add_argument("--sr", type=int, default=22050, help="Target sample rate")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"Error: not a directory: {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    audio_files = find_audio_files(args.input_dir)
    if not audio_files:
        print(f"No audio files found in {args.input_dir}")
        sys.exit(0)

    args.output.mkdir(parents=True, exist_ok=True)
    print(f"Found {len(audio_files)} audio file(s)")

    for i, audio_path in enumerate(audio_files, 1):
        print(f"  [{i}/{len(audio_files)}] {audio_path.name} ...", end=" ", flush=True)
        try:
            y, sr = librosa.load(str(audio_path), sr=args.sr, mono=True)
            summary = summarize(y, sr=sr)
            out_path = args.output / f"{audio_path.stem}.json"
            save_json(
                {
                    "file": str(audio_path),
                    "duration_s": summary.duration_s,
                    "tempo_bpm": summary.tempo_bpm,
                    "onset_count": summary.onset_count,
                    "rms_mean": summary.rms_mean,
                    "spectral_centroid_mean": summary.spectral_centroid_mean,
                    "tags": summary.tags,
                },
                out_path,
            )
            print("OK")
        except Exception as exc:
            print(f"FAIL ({exc})")

    print(f"\nResults saved to {args.output}/")


if __name__ == "__main__":
    main()

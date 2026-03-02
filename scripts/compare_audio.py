#!/usr/bin/env python3
"""Compare two audio files and display a side-by-side feature diff.

Usage:
    python scripts/compare_audio.py song_a.wav song_b.mp3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import librosa

from bird_mach.analysis import summarize
from bird_mach.compare import compare


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare two audio files side by side.",
    )
    parser.add_argument("file_a", type=Path, help="First audio file")
    parser.add_argument("file_b", type=Path, help="Second audio file")
    parser.add_argument("--sr", type=int, default=22050, help="Target sample rate")
    args = parser.parse_args()

    for f in (args.file_a, args.file_b):
        if not f.exists():
            print(f"Error: file not found: {f}", file=sys.stderr)
            sys.exit(1)

    print(f"Loading {args.file_a.name} ...")
    y_a, sr = librosa.load(str(args.file_a), sr=args.sr, mono=True)
    summary_a = summarize(y_a, sr=sr)

    print(f"Loading {args.file_b.name} ...")
    y_b, _ = librosa.load(str(args.file_b), sr=args.sr, mono=True)
    summary_b = summarize(y_b, sr=sr)

    result = compare(summary_a, summary_b)
    diff = result.to_dict()

    header = f"{'Feature':<30} {'A':>12} {'B':>12} {'Diff':>12}"
    print(f"\n{header}")
    print("-" * len(header))
    for field, vals in diff.items():
        print(f"{field:<30} {vals['a']:>12.4f} {vals['b']:>12.4f} {vals['diff']:>+12.4f}")

    print(f"\nTags A: {', '.join(summary_a.tags) or 'none'}")
    print(f"Tags B: {', '.join(summary_b.tags) or 'none'}")


if __name__ == "__main__":
    main()

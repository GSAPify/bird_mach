#!/usr/bin/env python3
"""Cluster audio frames and print segment breakdown.

Usage:
    python scripts/cluster_audio.py recording.wav --n-clusters 4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import librosa

from bird_mach.embedding import (
    AudioFeatureConfig,
    extract_log_mel_frames,
    stride_downsample,
)
from bird_mach.clustering import cluster_kmeans


def main() -> None:
    parser = argparse.ArgumentParser(description="Cluster audio frames.")
    parser.add_argument("audio_path", type=Path)
    parser.add_argument("--sr", type=int, default=22050)
    parser.add_argument("--n-clusters", type=int, default=5)
    parser.add_argument("--stride", type=int, default=2)
    args = parser.parse_args()

    if not args.audio_path.exists():
        print(f"Error: {args.audio_path} not found", file=sys.stderr)
        sys.exit(1)

    y, sr = librosa.load(str(args.audio_path), sr=args.sr, mono=True)
    cfg = AudioFeatureConfig()
    X, times, energy = extract_log_mel_frames(y, sr=sr, cfg=cfg)
    X, times, energy = stride_downsample(X, times, energy, stride=args.stride)

    result = cluster_kmeans(X, n_clusters=args.n_clusters)

    print(f"Frames: {len(result.labels)}")
    print(f"Clusters: {result.n_clusters}")
    print(f"Inertia: {result.inertia:.2f}")
    print()
    for label, count in sorted(result.label_counts.items()):
        pct = 100.0 * count / len(result.labels)
        print(f"  Cluster {label}: {count} frames ({pct:.1f}%)")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

from bird_mach.embedding import (
    AudioFeatureConfig,
    UmapConfig,
    build_multiview_figure,
    build_singleview_figure,
    compute_umap_3d,
    extract_log_mel_frames,
    load_audio_mono_from_path,
    stride_downsample,
)


DEFAULT_AUDIO_FEATURE_CONFIG = AudioFeatureConfig()
DEFAULT_UMAP_CONFIG = UmapConfig()

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create a 3D bird-sound embedding visualization (UMAP + Plotly).")
    p.add_argument("--input", required=True, type=Path, help="Path to input WAV/audio file.")
    p.add_argument("--output", required=True, type=Path, help="Path to output HTML.")
    p.add_argument("--multi-view", action="store_true", help="Render 3 stacked views (like the screenshot).")
    p.add_argument("--connect", action="store_true", help="Draw lines connecting points over time.")
    p.add_argument(
        "--color-by",
        choices=("time", "energy"),
        default="time",
        help="Color points by time (seconds) or energy.",
    )
    p.add_argument("--stride", type=int, default=2, help="Downsample frames by taking every Nth frame.")

    p.add_argument("--sr", type=int, default=DEFAULT_AUDIO_FEATURE_CONFIG.sr)
    p.add_argument("--n-fft", type=int, default=DEFAULT_AUDIO_FEATURE_CONFIG.n_fft)
    p.add_argument("--hop-length", type=int, default=DEFAULT_AUDIO_FEATURE_CONFIG.hop_length)
    p.add_argument("--n-mels", type=int, default=DEFAULT_AUDIO_FEATURE_CONFIG.n_mels)
    p.add_argument("--fmin", type=float, default=DEFAULT_AUDIO_FEATURE_CONFIG.fmin)
    p.add_argument("--fmax", type=float, default=DEFAULT_AUDIO_FEATURE_CONFIG.fmax)

    p.add_argument("--n-neighbors", type=int, default=DEFAULT_UMAP_CONFIG.n_neighbors)
    p.add_argument("--min-dist", type=float, default=DEFAULT_UMAP_CONFIG.min_dist)
    p.add_argument("--metric", type=str, default=DEFAULT_UMAP_CONFIG.metric)
    p.add_argument("--random-state", type=int, default=DEFAULT_UMAP_CONFIG.random_state)

    return p.parse_args()


def main() -> None:
    args = parse_args()

    audio_cfg = AudioFeatureConfig(
        sr=args.sr,
        n_fft=args.n_fft,
        hop_length=args.hop_length,
        n_mels=args.n_mels,
        fmin=args.fmin,
        fmax=args.fmax,
    )
    umap_cfg = UmapConfig(
        n_neighbors=args.n_neighbors,
        min_dist=args.min_dist,
        metric=args.metric,
        random_state=args.random_state,
    )

    y, sr = load_audio_mono_from_path(args.input, sr=audio_cfg.sr)
    X, times_s, energy = extract_log_mel_frames(y, sr, audio_cfg)
    X, times_s, energy = stride_downsample(X, times_s, energy, stride=args.stride)
    emb = compute_umap_3d(X, umap_cfg)

    title = f"{args.input.name} — 3D embedding ({X.shape[0]} frames)"
    color_by = args.color_by  # type: ignore[assignment]

    if args.multi_view:
        fig = build_multiview_figure(
            emb,
            times_s=times_s,
            energy=energy,
            color_by=color_by,
            connect=args.connect,
            title=title,
        )
    else:
        fig = build_singleview_figure(
            emb,
            times_s=times_s,
            energy=energy,
            color_by=color_by,
            connect=args.connect,
            title=title,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(args.output), include_plotlyjs="cdn")
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()



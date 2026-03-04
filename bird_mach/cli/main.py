"""Unified CLI entry point for Mach audio tools.

Usage:
    python -m bird_mach.cli.main analyze recording.wav
    python -m bird_mach.cli.main serve --port 8000
"""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mach",
        description="Mach — universal audio visualization toolkit",
    )
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze", help="Analyze an audio file")
    analyze.add_argument("audio_path", help="Path to audio file")
    analyze.add_argument("--sr", type=int, default=22050)
    analyze.add_argument("--output", "-o", help="Save JSON to file")

    serve = sub.add_parser("serve", help="Start the web server")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--reload", action="store_true")

    compare = sub.add_parser("compare", help="Compare two audio files")
    compare.add_argument("file_a", help="First audio file")
    compare.add_argument("file_b", help="Second audio file")

    sub.add_parser("version", help="Print version")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        from bird_mach.constants import APP_VERSION
        print(f"Mach v{APP_VERSION}")
    elif args.command == "serve":
        import uvicorn
        uvicorn.run(
            "bird_mach.webapp:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
    elif args.command is None:
        parser.print_help()
        sys.exit(1)
    else:
        print(f"Command '{args.command}' — use the standalone scripts for now.")


if __name__ == "__main__":
    main()

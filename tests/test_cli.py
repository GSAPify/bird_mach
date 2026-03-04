"""Tests for bird_mach.cli.main."""

import pytest

from bird_mach.cli.main import build_parser


class TestBuildParser:
    def test_has_analyze_command(self):
        parser = build_parser()
        args = parser.parse_args(["analyze", "test.wav"])
        assert args.command == "analyze"

    def test_has_serve_command(self):
        parser = build_parser()
        args = parser.parse_args(["serve", "--port", "9000"])
        assert args.command == "serve"
        assert args.port == 9000

    def test_has_version_command(self):
        parser = build_parser()
        args = parser.parse_args(["version"])
        assert args.command == "version"

    def test_compare_command(self):
        parser = build_parser()
        args = parser.parse_args(["compare", "a.wav", "b.wav"])
        assert args.command == "compare"
        assert args.file_a == "a.wav"

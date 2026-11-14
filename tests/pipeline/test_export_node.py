"""Tests for ExportNode."""
import pytest

from bird_mach.constants import SUPPORTED_EXPORT_FORMATS
from bird_mach.pipeline.nodes.export_node import ExportNode


def test_default_format_is_json():
    assert ExportNode().process({}) == {"exported": True, "format": "json"}


def test_every_supported_format_is_accepted():
    for fmt in SUPPORTED_EXPORT_FORMATS:
        assert ExportNode(fmt).process({})["format"] == fmt

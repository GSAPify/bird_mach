"""Tests for LoaderNode."""
import pytest

from bird_mach.pipeline.nodes.loader_node import LoaderNode


def test_default_sample_rate():
    assert LoaderNode().process({"path": "a.wav"}) == {"sr": 22050, "loaded": True}

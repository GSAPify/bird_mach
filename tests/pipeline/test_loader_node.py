"""Tests for LoaderNode."""
import pytest

from bird_mach.pipeline.nodes.loader_node import LoaderNode


def test_default_sample_rate():
    assert LoaderNode().process({"path": "a.wav"}) == {"sr": 22050, "loaded": True}


def test_custom_sample_rate():
    assert LoaderNode(sr=44100).process({"path": "a.wav"})["sr"] == 44100


def test_zero_sample_rate_is_rejected():
    with pytest.raises(ValueError):
        LoaderNode(sr=0)


def test_negative_sample_rate_is_rejected():
    with pytest.raises(ValueError):
        LoaderNode(sr=-1)

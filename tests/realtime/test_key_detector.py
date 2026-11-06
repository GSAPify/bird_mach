"""Tests for KeyDetector."""
import numpy as np

from bird_mach.realtime.key_detector import KEY_PROFILES, KeyDetector


def test_silence_is_unknown_key():
    assert KeyDetector().detect(np.zeros(12))["key"] == "unknown"


def test_major_profile_detects_c_major():
    result = KeyDetector().detect(np.array(KEY_PROFILES["major"]))
    assert (result["key"], result["mode"]) == ("C", "major")

"""Tests for SDK helper variant 4."""
from bird_mach.sdk.helpers_v4 import format_result_v4, validate_params_v4


def test_format_result_sorts_keys_and_joins_with_pipes():
    assert format_result_v4({"b": 2, "a": 1}) == "a: 1 | b: 2"

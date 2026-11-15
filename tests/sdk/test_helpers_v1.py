"""Tests for SDK helper variant 1."""
from bird_mach.sdk.helpers_v1 import format_result_v1, validate_params_v1


def test_format_result_sorts_keys_and_joins_with_pipes():
    assert format_result_v1({"b": 2, "a": 1}) == "a: 1 | b: 2"

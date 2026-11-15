"""Tests for SDK helper variant 2."""
from bird_mach.sdk.helpers_v2 import format_result_v2, validate_params_v2


def test_format_result_sorts_keys_and_joins_with_pipes():
    assert format_result_v2({"b": 2, "a": 1}) == "a: 1 | b: 2"


def test_format_result_of_empty_dict_is_empty_string():
    assert format_result_v2({}) == ""

"""Tests for SDK helper variant 1."""
from bird_mach.sdk.helpers_v1 import format_result_v1, validate_params_v1


def test_format_result_sorts_keys_and_joins_with_pipes():
    assert format_result_v1({"b": 2, "a": 1}) == "a: 1 | b: 2"


def test_format_result_of_empty_dict_is_empty_string():
    assert format_result_v1({}) == ""


def test_validate_params_requires_non_blank_string_path():
    assert validate_params_v1(path="a.wav") is True
    assert validate_params_v1(path="a.wav", extra=1) is True
    assert validate_params_v1() is False
    assert validate_params_v1(path="   ") is False
    assert validate_params_v1(path=5) is False

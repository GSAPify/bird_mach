"""Tests for SDKResponse."""
import pytest

from bird_mach.sdk.response import SDKResponse


def test_defaults_describe_a_successful_response():
    resp = SDKResponse(success=True)
    assert resp.data == {} and resp.error is None
    assert resp.status_code == 200 and not resp.is_error


def test_unsuccessful_response_is_error():
    assert SDKResponse(success=False).is_error


def test_http_error_status_is_error_even_if_success_flag_set():
    assert SDKResponse(success=True, status_code=500).is_error
    assert not SDKResponse(success=True, status_code=399).is_error


def test_raise_for_status_messages():
    with pytest.raises(RuntimeError, match="nope"):
        SDKResponse(success=False, error="nope").raise_for_status()
    with pytest.raises(RuntimeError, match="status 404"):
        SDKResponse(success=True, status_code=404).raise_for_status()
    SDKResponse(success=True).raise_for_status()

"""Tests for SDKResponse."""
import pytest

from bird_mach.sdk.response import SDKResponse


def test_defaults_describe_a_successful_response():
    resp = SDKResponse(success=True)
    assert resp.data == {} and resp.error is None
    assert resp.status_code == 200 and not resp.is_error


def test_unsuccessful_response_is_error():
    assert SDKResponse(success=False).is_error

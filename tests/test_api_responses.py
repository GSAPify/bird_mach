"""Tests for standardized API response helpers."""
import json

from bird_mach.api.responses import error, success


def test_success_wraps_data():
    resp = success({"a": 1})
    assert resp.status_code == 200
    assert json.loads(resp.body) == {"status": "ok", "data": {"a": 1}}


def test_success_accepts_custom_status():
    assert success({}, status_code=201).status_code == 201

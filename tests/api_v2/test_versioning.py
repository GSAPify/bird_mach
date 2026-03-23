"""Tests for API versioning."""
from bird_mach.api.v2.versioning import parse_version, is_deprecated, deprecation_header

class TestVersioning:
    def test_parse_v2(self):
        assert parse_version("application/json; version=2") == "v2"

    def test_parse_v1(self):
        assert parse_version("application/json; version=1") == "v1"

    def test_default(self):
        assert parse_version("application/json") == "v2"

    def test_deprecated(self):
        assert is_deprecated("v1")
        assert not is_deprecated("v2")

    def test_deprecation_header(self):
        h = deprecation_header("v1")
        assert "Deprecation" in h
        assert deprecation_header("v2") == {}

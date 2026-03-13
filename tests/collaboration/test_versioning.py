"""Tests for config versioning."""
from bird_mach.collaboration.versioning import ConfigVersioning
class TestVersioning:
    def test_commit(self):
        cv = ConfigVersioning()
        v = cv.commit({"sr": 22050}, "u1", "initial")
        assert v.version == 1
    def test_get(self):
        cv = ConfigVersioning()
        cv.commit({"a": 1}, "u1", "v1")
        assert cv.get(1).config == {"a": 1}
    def test_diff(self):
        cv = ConfigVersioning()
        cv.commit({"a": 1, "b": 2}, "u1", "v1")
        cv.commit({"a": 1, "b": 3}, "u1", "v2")
        d = cv.diff(1, 2)
        assert "b" in d

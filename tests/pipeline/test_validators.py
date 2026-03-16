"""Tests for pipeline validators."""
from bird_mach.pipeline.validators import validate_pipeline_input

class TestValidators:
    def test_valid(self):
        assert validate_pipeline_input({"path": "test.wav", "sr": 22050}) == []

    def test_bad_sr(self):
        errors = validate_pipeline_input({"sr": 100})
        assert len(errors) == 1

    def test_no_extension(self):
        errors = validate_pipeline_input({"path": "noext"})
        assert len(errors) == 1

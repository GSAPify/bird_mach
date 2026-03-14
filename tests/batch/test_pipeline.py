"""Tests for batch pipeline."""
from pathlib import Path
from bird_mach.batch.pipeline import BatchPipeline

class TestBatchPipeline:
    def test_empty_pipeline(self, tmp_path):
        pipe = BatchPipeline()
        f = tmp_path / "test.wav"
        f.write_bytes(b"data")
        result = pipe.process_file(f)
        assert result.success

    def test_add_step(self):
        pipe = BatchPipeline()
        pipe.add_step("test", lambda p, o: {"ok": True})
        assert pipe.step_count == 1

    def test_step_failure(self, tmp_path):
        pipe = BatchPipeline()
        pipe.add_step("fail", lambda p, o: 1 / 0)
        f = tmp_path / "test.wav"
        f.write_bytes(b"data")
        result = pipe.process_file(f)
        assert not result.success

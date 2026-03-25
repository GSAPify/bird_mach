"""Tests for file scanner."""
from pathlib import Path
from bird_mach.batch.file_scanner import scan_directory, group_by_format

class TestFileScanner:
    def test_scan(self, tmp_path):
        (tmp_path / "a.wav").write_bytes(b"x")
        (tmp_path / "b.mp3").write_bytes(b"x")
        (tmp_path / "c.txt").write_bytes(b"x")
        files = scan_directory(tmp_path)
        assert len(files) == 2

    def test_group(self, tmp_path):
        files = [Path("a.wav"), Path("b.wav"), Path("c.mp3")]
        groups = group_by_format(files)
        assert len(groups[".wav"]) == 2
        assert len(groups[".mp3"]) == 1

    def test_non_recursive(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.wav").write_bytes(b"x")
        (sub / "b.wav").write_bytes(b"x")
        files = scan_directory(tmp_path, recursive=False)
        assert len(files) == 1

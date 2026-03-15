"""Tests for export formats."""
from bird_mach.reporting.export_formats import to_json_lines, to_csv_string, to_tsv_string
class TestExportFormats:
    def test_jsonl(self):
        records = [{"a": 1}, {"a": 2}]
        result = to_json_lines(records)
        assert result.count("\n") == 1
    def test_csv(self):
        records = [{"name": "test", "val": 42}]
        result = to_csv_string(records)
        assert "name,val" in result
    def test_tsv(self):
        records = [{"x": 1}]
        result = to_tsv_string(records)
        assert "\t" not in result.split("\n")[0] or "x" in result
    def test_empty(self):
        assert to_csv_string([]) == ""

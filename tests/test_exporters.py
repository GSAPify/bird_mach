"""Tests for bird_mach.exporters."""

from __future__ import annotations

import json

import numpy as np

from bird_mach.exporters import to_json, features_to_csv, summary_to_html


class TestToJson:
    def test_serializes_numpy_arrays(self):
        data = {"values": np.array([1.0, 2.0, 3.0])}
        result = to_json(data)
        parsed = json.loads(result)
        assert parsed["values"] == [1.0, 2.0, 3.0]

    def test_serializes_numpy_scalars(self):
        data = {"mean": np.float32(3.14)}
        result = to_json(data)
        parsed = json.loads(result)
        assert abs(parsed["mean"] - 3.14) < 0.01

    def test_roundtrip(self):
        original = {"name": "test", "score": 0.95, "tags": ["a", "b"]}
        result = json.loads(to_json(original))
        assert result == original

    def test_serializes_numpy_bool(self):
        data = {"is_silent": np.bool_(False), "has_onset": np.bool_(True)}
        result = json.loads(to_json(data))
        assert result["is_silent"] is False
        assert result["has_onset"] is True


class TestFeaturesToCsv:
    def test_header_and_rows(self):
        times = np.array([0.0, 0.5, 1.0])
        cols = {"energy": np.array([0.1, 0.5, 0.3])}
        csv_str = features_to_csv(times, columns=cols)
        lines = csv_str.strip().split("\n")
        assert lines[0] == "time_s,energy"
        assert len(lines) == 4

    def test_multiple_columns(self):
        times = np.array([0.0, 1.0])
        cols = {
            "energy": np.array([0.5, 0.8]),
            "zcr": np.array([0.1, 0.2]),
        }
        csv_str = features_to_csv(times, columns=cols)
        header = csv_str.strip().split("\n")[0]
        assert "energy" in header
        assert "zcr" in header


class TestSummaryToHtml:
    def test_contains_title(self):
        html = summary_to_html({"bpm": 120}, title="My Report")
        assert "My Report" in html

    def test_contains_key_and_value(self):
        html = summary_to_html({"tempo": "120 bpm"})
        assert "tempo" in html
        assert "120 bpm" in html

    def test_escapes_special_chars_in_title(self):
        html = summary_to_html({}, title="<script>alert(1)</script>")
        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    def test_escapes_special_chars_in_values(self):
        html = summary_to_html({"<key>": "<value>"})
        assert "<key>" not in html.split("<table>")[1]
        assert "&lt;key&gt;" in html
        assert "&lt;value&gt;" in html

"""Tests for report generation."""
from bird_mach.reporting.pdf_report import AnalysisReport

class TestAnalysisReport:
    def test_create(self):
        r = AnalysisReport("Test Report")
        assert r.title == "Test Report"
        assert r.section_count == 0

    def test_add_section(self):
        r = AnalysisReport("Test")
        r.add_section("Overview", "This is a test.")
        assert r.section_count == 1

    def test_to_markdown(self):
        r = AnalysisReport("Test")
        r.add_section("Intro", "Hello world")
        md = r.to_markdown()
        assert "# Test" in md
        assert "Hello world" in md

    def test_to_dict(self):
        r = AnalysisReport("Test")
        r.add_section("S1", "Content")
        d = r.to_dict()
        assert d["title"] == "Test"
        assert len(d["sections"]) == 1

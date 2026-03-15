"""Tests for HTML report renderer."""
from bird_mach.reporting.pdf_report import AnalysisReport
from bird_mach.reporting.html_report import HTMLReportRenderer
class TestHTMLRenderer:
    def test_render(self):
        r = AnalysisReport("Test")
        r.add_section("Intro", "Hello")
        html = HTMLReportRenderer().render(r)
        assert "<h1>Test</h1>" in html
        assert "Hello" in html

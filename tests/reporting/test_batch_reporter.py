"""Tests for BatchReporter."""
from bird_mach.reporting.batch_reporter import BatchReporter
from bird_mach.reporting.pdf_report import AnalysisReport


def make_report(title, sections=0):
    report = AnalysisReport(title)
    for i in range(sections):
        report.add_section(f"S{i}", "body")
    return report


def test_empty_reporter_summary(tmp_path):
    reporter = BatchReporter(tmp_path)
    summary = reporter.generate_summary()
    assert reporter.report_count == 0
    assert summary.startswith("# Batch Analysis Summary")
    assert "Total files: 0" in summary

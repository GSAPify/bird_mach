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


def test_add_report_increments_count(tmp_path):
    reporter = BatchReporter(tmp_path)
    reporter.add_report(make_report("A"))
    reporter.add_report(make_report("B"))
    assert reporter.report_count == 2


def test_summary_lists_titles_in_order(tmp_path):
    reporter = BatchReporter(tmp_path)
    reporter.add_report(make_report("First"))
    reporter.add_report(make_report("Second"))
    summary = reporter.generate_summary()
    assert summary.index("## 1. First") < summary.index("## 2. Second")


def test_summary_includes_section_counts(tmp_path):
    reporter = BatchReporter(tmp_path)
    reporter.add_report(make_report("A", sections=3))
    assert "Sections: 3" in reporter.generate_summary()


def test_save_all_creates_directory_and_numbered_files(tmp_path):
    out = tmp_path / "nested" / "reports"
    reporter = BatchReporter(out)
    reporter.add_report(make_report("A"))
    reporter.add_report(make_report("B"))
    paths = reporter.save_all()
    assert [p.name for p in paths] == ["report_0000.md", "report_0001.md"]
    assert all(p.exists() for p in paths)


def test_saved_file_matches_markdown(tmp_path):
    reporter = BatchReporter(tmp_path)
    report = make_report("A", sections=2)
    reporter.add_report(report)
    (path,) = reporter.save_all()
    assert path.read_text(encoding="utf-8") == report.to_markdown()

"""Batch report generation for multiple audio files."""
from __future__ import annotations
from pathlib import Path
from bird_mach.reporting.pdf_report import AnalysisReport

class BatchReporter:
    """Generate comparison reports across multiple audio files."""

    def __init__(self, output_dir: Path):
        self._output_dir = output_dir
        self._reports: list[AnalysisReport] = []

    def add_report(self, report: AnalysisReport) -> None:
        self._reports.append(report)

    def generate_summary(self) -> str:
        lines = ["# Batch Analysis Summary", f"Total files: {len(self._reports)}", ""]
        for i, r in enumerate(self._reports, 1):
            lines.append(f"## {i}. {r.title}")
            lines.append(f"Sections: {r.section_count}")
            lines.append("")
        return "\n".join(lines)

    def save_all(self) -> list[Path]:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for i, report in enumerate(self._reports):
            path = self._output_dir / f"report_{i:04d}.md"
            path.write_text(report.to_markdown(), encoding="utf-8")
            paths.append(path)
        return paths

    @property
    def report_count(self) -> int:
        return len(self._reports)

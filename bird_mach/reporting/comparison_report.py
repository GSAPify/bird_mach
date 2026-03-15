"""Generate comparison reports between two audio files."""
from __future__ import annotations
from bird_mach.reporting.pdf_report import AnalysisReport
from bird_mach.analysis import AnalysisSummary

def build_comparison_report(name_a: str, summary_a: AnalysisSummary,
                            name_b: str, summary_b: AnalysisSummary) -> AnalysisReport:
    report = AnalysisReport(f"Comparison: {name_a} vs {name_b}")
    report.add_section("Overview", f"Comparing {name_a} ({summary_a.duration_s:.1f}s) with {name_b} ({summary_b.duration_s:.1f}s)")
    tempo_diff = summary_b.tempo_bpm - summary_a.tempo_bpm
    report.add_section("Tempo", f"{name_a}: {summary_a.tempo_bpm:.1f} BPM | {name_b}: {summary_b.tempo_bpm:.1f} BPM | Diff: {tempo_diff:+.1f}")
    energy_diff = summary_b.rms_mean - summary_a.rms_mean
    report.add_section("Energy", f"{name_a}: {summary_a.rms_mean:.4f} | {name_b}: {summary_b.rms_mean:.4f} | Diff: {energy_diff:+.4f}")
    return report

# Reporting

## Report Types
- **Analysis Report**: Single file deep-dive
- **Comparison Report**: A/B analysis
- **Batch Report**: Multi-file summary

## Export Formats
- Markdown, HTML, JSON, JSONL, CSV, TSV

## Scheduled Reports
Configure daily/weekly/monthly automated reports with email delivery.

## Usage
```python
from bird_mach.reporting.pdf_report import AnalysisReport
report = AnalysisReport("My Analysis")
report.add_section("Summary", "Key findings...")
print(report.to_markdown())
```

"""Scheduled report generation configuration."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Schedule(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class ScheduledReport:
    name: str
    schedule: Schedule
    recipients: list[str]
    query: str
    format: str = "html"
    enabled: bool = True

class ReportScheduler:
    def __init__(self):
        self._schedules: list[ScheduledReport] = []

    def add(self, report: ScheduledReport) -> None:
        self._schedules.append(report)

    def get_due(self, schedule: Schedule) -> list[ScheduledReport]:
        return [r for r in self._schedules if r.schedule == schedule and r.enabled]

    @property
    def count(self) -> int:
        return len(self._schedules)

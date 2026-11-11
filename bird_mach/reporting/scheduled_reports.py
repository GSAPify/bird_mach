"""Scheduled report generation configuration."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
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
    last_sent: datetime | None = None

SCHEDULE_INTERVALS = {
    Schedule.DAILY: timedelta(days=1),
    Schedule.WEEKLY: timedelta(days=7),
    Schedule.MONTHLY: timedelta(days=30),
}

class ReportScheduler:
    def __init__(self):
        self._schedules: list[ScheduledReport] = []

    def add(self, report: ScheduledReport) -> None:
        self._schedules.append(report)

    def get_due(self, schedule: Schedule, now: datetime | None = None) -> list[ScheduledReport]:
        # Ignoring last_sent meant every scheduler run re-sent every report.
        now = now or datetime.now(timezone.utc)
        interval = SCHEDULE_INTERVALS[schedule]
        return [
            r for r in self._schedules
            if r.schedule == schedule and r.enabled
            and (r.last_sent is None or now - r.last_sent >= interval)
        ]

    def mark_sent(self, report: ScheduledReport, when: datetime | None = None) -> None:
        report.last_sent = when or datetime.now(timezone.utc)

    @property
    def count(self) -> int:
        return len(self._schedules)

"""Tests for ReportScheduler."""
from datetime import datetime, timedelta, timezone

from bird_mach.reporting.scheduled_reports import ReportScheduler, Schedule, ScheduledReport


def make(schedule=Schedule.DAILY):
    return ScheduledReport(name="r", schedule=schedule, recipients=["a@x.io"], query="q")


def test_never_sent_report_is_due():
    sched = ReportScheduler()
    sched.add(make())
    assert len(sched.get_due(Schedule.DAILY)) == 1


def test_just_sent_report_is_not_due_until_interval_passes():
    sched = ReportScheduler()
    report = make()
    sched.add(report)
    sent = datetime(2026, 11, 1, tzinfo=timezone.utc)
    sched.mark_sent(report, when=sent)
    assert sched.get_due(Schedule.DAILY, now=sent + timedelta(hours=1)) == []
    assert sched.get_due(Schedule.DAILY, now=sent + timedelta(days=1)) == [report]

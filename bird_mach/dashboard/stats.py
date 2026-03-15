"""Dashboard statistics aggregation."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class DashboardStats:
    total_analyses: int
    total_audio_hours: float
    active_projects: int
    active_users: int
    avg_analysis_time_ms: float
    top_formats: dict[str, int]
    analyses_today: int
    analyses_this_week: int

class StatsAggregator:
    def __init__(self):
        self._analyses: list[dict] = []

    def record(self, duration_s: float, format: str, processing_ms: float):
        self._analyses.append({
            "duration_s": duration_s, "format": format,
            "processing_ms": processing_ms, "timestamp": datetime.now(),
        })

    def compute(self) -> DashboardStats:
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0)
        week_ago = now - timedelta(days=7)

        formats: dict[str, int] = {}
        total_hours = 0.0
        total_ms = 0.0
        today_count = 0
        week_count = 0

        for a in self._analyses:
            total_hours += a["duration_s"] / 3600
            total_ms += a["processing_ms"]
            fmt = a["format"]
            formats[fmt] = formats.get(fmt, 0) + 1
            if a["timestamp"] >= today:
                today_count += 1
            if a["timestamp"] >= week_ago:
                week_count += 1

        avg_ms = total_ms / max(len(self._analyses), 1)
        return DashboardStats(
            total_analyses=len(self._analyses),
            total_audio_hours=round(total_hours, 2),
            active_projects=0, active_users=0,
            avg_analysis_time_ms=round(avg_ms, 1),
            top_formats=dict(sorted(formats.items(), key=lambda x: -x[1])[:5]),
            analyses_today=today_count,
            analyses_this_week=week_count,
        )

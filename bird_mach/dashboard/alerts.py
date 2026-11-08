"""Alert rules and notification triggers."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class AlertRule:
    name: str
    metric: str
    threshold: float
    severity: AlertSeverity
    enabled: bool = True

class AlertManager:
    def __init__(self, max_history: int = 1000):
        self._rules: list[AlertRule] = []
        # Bounded: a monitor evaluating every second over threshold used to
        # append 86,400 dicts a day with no limit.
        self._fired: deque[dict] = deque(maxlen=max_history)
        self._total_fired = 0

    def add_rule(self, rule: AlertRule) -> None:
        self._rules.append(rule)

    def evaluate(self, metrics: dict[str, float]) -> list[dict]:
        alerts = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            if rule.metric not in metrics:
                continue
            value = metrics[rule.metric]
            if value >= rule.threshold:
                alert = {"rule": rule.name, "value": value, "threshold": rule.threshold, "severity": rule.severity.value}
                alerts.append(alert)
                self._fired.append(alert)
                self._total_fired += 1
        return alerts

    @property
    def total_fired(self) -> int:
        return self._total_fired

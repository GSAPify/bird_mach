"""Alert rules and notification triggers."""
from __future__ import annotations
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
    def __init__(self):
        self._rules: list[AlertRule] = []
        self._fired: list[dict] = []

    def add_rule(self, rule: AlertRule) -> None:
        self._rules.append(rule)

    def evaluate(self, metrics: dict[str, float]) -> list[dict]:
        alerts = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            value = metrics.get(rule.metric, 0)
            if value > rule.threshold:
                alert = {"rule": rule.name, "value": value, "threshold": rule.threshold, "severity": rule.severity.value}
                alerts.append(alert)
                self._fired.append(alert)
        return alerts

    @property
    def total_fired(self) -> int:
        return len(self._fired)

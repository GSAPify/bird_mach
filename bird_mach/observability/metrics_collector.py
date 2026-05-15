"""Prometheus-style metrics collection."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Metric:
    name: str
    type: str
    value: float
    labels: dict[str, str]
    timestamp: float

class MetricsCollector:
    def __init__(self):
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)

    def inc(self, name: str, value: float = 1.0, **labels) -> None:
        key = self._key(name, labels)
        self._counters[key] += value

    def set_gauge(self, name: str, value: float, **labels) -> None:
        key = self._key(name, labels)
        self._gauges[key] = value

    def observe(self, name: str, value: float, **labels) -> None:
        key = self._key(name, labels)
        self._histograms[key].append(value)

    def get_counter(self, name: str, **labels) -> float:
        return self._counters.get(self._key(name, labels), 0.0)

    def get_gauge(self, name: str, **labels) -> float:
        return self._gauges.get(self._key(name, labels), 0.0)

    def get_histogram_avg(self, name: str, **labels) -> float:
        vals = self._histograms.get(self._key(name, labels), [])
        return sum(vals) / max(len(vals), 1)

    def export_prometheus(self) -> str:
        lines = []
        for key, val in sorted(self._counters.items()):
            lines.append(f"{key} {val}")
        for key, val in sorted(self._gauges.items()):
            lines.append(f"{key} {val}")
        return "\n".join(lines)

    @staticmethod
    def _key(name: str, labels: dict[str, str]) -> str:
        if not labels:
            return name
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

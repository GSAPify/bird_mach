# Observability

## Metrics
Prometheus-style counters, gauges, and histograms.

```python
from bird_mach.observability.metrics_collector import MetricsCollector
mc = MetricsCollector()
mc.inc("requests_total", method="GET")
mc.observe("latency_ms", 45.0)
print(mc.export_prometheus())
```

## Tracing
Distributed tracing with parent-child span hierarchy.

## Health Checks
Pluggable health checks for dependencies (DB, cache, external APIs).

## Structured Logging
JSON-formatted logs with trace ID correlation.

## SLA Tracking
Uptime percentage and p99 response time monitoring.

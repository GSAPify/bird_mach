"""Tests for alert manager."""
from bird_mach.dashboard.alerts import AlertManager, AlertRule, AlertSeverity
class TestAlertManager:
    def test_no_alerts(self):
        mgr = AlertManager()
        mgr.add_rule(AlertRule("high_cpu", "cpu", 90.0, AlertSeverity.WARNING))
        alerts = mgr.evaluate({"cpu": 50.0})
        assert len(alerts) == 0
    def test_fires_alert(self):
        mgr = AlertManager()
        mgr.add_rule(AlertRule("high_cpu", "cpu", 90.0, AlertSeverity.CRITICAL))
        alerts = mgr.evaluate({"cpu": 95.0})
        assert len(alerts) == 1
        assert alerts[0]["severity"] == "critical"


def test_fired_history_is_bounded_but_total_counts_all():
    from bird_mach.dashboard.alerts import AlertManager, AlertRule, AlertSeverity
    mgr = AlertManager(max_history=2)
    mgr.add_rule(AlertRule("cpu", "cpu", 0.9, AlertSeverity.WARNING))
    for _ in range(5):
        mgr.evaluate({"cpu": 0.95})
    assert mgr.total_fired == 5
    assert len(mgr._fired) == 2

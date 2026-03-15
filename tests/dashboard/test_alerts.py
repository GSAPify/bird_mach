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

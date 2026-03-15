"""Tests for notification service."""
from bird_mach.notifications_service import NotificationService, NotificationType

class TestNotificationService:
    def test_send(self):
        svc = NotificationService()
        n = svc.send("u1", NotificationType.INFO, "Welcome", "Hello!")
        assert n.title == "Welcome"

    def test_unread_count(self):
        svc = NotificationService()
        svc.send("u1", NotificationType.INFO, "N1", "msg1")
        svc.send("u1", NotificationType.SUCCESS, "N2", "msg2")
        assert svc.unread_count("u1") == 2

    def test_mark_read(self):
        svc = NotificationService()
        n = svc.send("u1", NotificationType.INFO, "Test", "msg")
        svc.mark_read("u1", n.id)
        assert svc.unread_count("u1") == 0

    def test_mark_all_read(self):
        svc = NotificationService()
        for i in range(5):
            svc.send("u1", NotificationType.INFO, f"N{i}", "msg")
        count = svc.mark_all_read("u1")
        assert count == 5
        assert svc.unread_count("u1") == 0

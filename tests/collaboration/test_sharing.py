"""Tests for sharing service."""
from bird_mach.collaboration.sharing import SharingService

class TestSharingService:
    def test_create_link(self):
        svc = SharingService()
        link = svc.create_link("audio1", "user1")
        assert link.token
        assert link.audio_id == "audio1"

    def test_access_valid(self):
        svc = SharingService()
        link = svc.create_link("audio1", "user1")
        result = svc.access(link.token)
        assert result is not None
        assert result.view_count == 1

    def test_access_with_password(self):
        svc = SharingService()
        link = svc.create_link("audio1", "user1", password="secret")
        assert svc.access(link.token) is None
        assert svc.access(link.token, password="secret") is not None

    def test_max_views(self):
        svc = SharingService()
        link = svc.create_link("audio1", "user1", max_views=2)
        svc.access(link.token)
        svc.access(link.token)
        assert svc.access(link.token) is None

    def test_revoke(self):
        svc = SharingService()
        link = svc.create_link("audio1", "user1")
        assert svc.revoke(link.token)
        assert svc.access(link.token) is None

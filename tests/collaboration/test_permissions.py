"""Tests for permissions."""
from bird_mach.collaboration.permissions import has_permission, Permission
class TestPermissions:
    def test_viewer_can_view(self):
        assert has_permission("viewer", Permission.VIEW)
    def test_viewer_cannot_edit(self):
        assert not has_permission("viewer", Permission.EDIT)
    def test_admin_can_all(self):
        assert has_permission("admin", Permission.ADMIN)
    def test_editor_can_annotate(self):
        assert has_permission("editor", Permission.ANNOTATE)

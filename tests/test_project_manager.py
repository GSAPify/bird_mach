"""Tests for project manager."""
from bird_mach.project_manager import ProjectManager

class TestProjectManager:
    def test_create(self):
        pm = ProjectManager()
        p = pm.create("My Project", "user1", "Test project")
        assert p.name == "My Project"

    def test_list_for_user(self):
        pm = ProjectManager()
        pm.create("P1", "user1")
        pm.create("P2", "user2")
        assert len(pm.list_for_user("user1")) == 1

    def test_archive(self):
        pm = ProjectManager()
        p = pm.create("P1", "user1")
        pm.archive(p.id)
        assert len(pm.list_for_user("user1")) == 0

    def test_add_audio(self):
        pm = ProjectManager()
        p = pm.create("P1", "user1")
        p.add_audio("audio-1")
        assert "audio-1" in p.audio_ids

    def test_search(self):
        pm = ProjectManager()
        pm.create("Music Analysis", "u1")
        pm.create("Speech Test", "u1")
        results = pm.search("music")
        assert len(results) == 1

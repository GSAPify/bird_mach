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

    def test_search_empty_query_returns_empty(self):
        """Empty query must not silently return all projects."""
        pm = ProjectManager()
        pm.create("Music Analysis", "u1")
        assert pm.search("") == []
        assert pm.search("   ") == []

    def test_search_excludes_archived(self):
        pm = ProjectManager()
        p = pm.create("Archive Me", "u1")
        pm.archive(p.id)
        assert pm.search("archive") == []

    def test_search_matches_tags(self):
        pm = ProjectManager()
        p = pm.create("My Project", "u1")
        p.tags.append("birdsong")
        results = pm.search("birdsong")
        assert any(r.id == p.id for r in results)

    def test_delete(self):
        pm = ProjectManager()
        p = pm.create("Throwaway", "u1")
        assert pm.delete(p.id) is True
        assert pm.get(p.id) is None

    def test_delete_nonexistent_returns_false(self):
        pm = ProjectManager()
        assert pm.delete("does-not-exist") is False

    def test_add_audio_no_duplicates(self):
        pm = ProjectManager()
        p = pm.create("P1", "u1")
        p.add_audio("audio-1")
        p.add_audio("audio-1")
        assert p.audio_ids.count("audio-1") == 1

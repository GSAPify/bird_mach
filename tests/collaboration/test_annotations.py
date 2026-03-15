"""Tests for annotations."""
from bird_mach.collaboration.annotations import AnnotationStore

class TestAnnotationStore:
    def test_add_annotation(self):
        store = AnnotationStore()
        ann = store.add("room1", "user1", 5.0, 2.0, "Nice section!")
        assert ann.text == "Nice section!"

    def test_get_sorted(self):
        store = AnnotationStore()
        store.add("room1", "u1", 10.0, 1.0, "Second")
        store.add("room1", "u1", 2.0, 1.0, "First")
        anns = store.get_for_room("room1")
        assert anns[0].timestamp_s < anns[1].timestamp_s

    def test_delete(self):
        store = AnnotationStore()
        ann = store.add("room1", "u1", 5.0, 1.0, "Delete me")
        assert store.delete("room1", ann.id)
        assert len(store.get_for_room("room1")) == 0

    def test_reactions(self):
        store = AnnotationStore()
        ann = store.add("room1", "u1", 5.0, 1.0, "Great!")
        ann.add_reaction("👍", "u2")
        assert "u2" in ann.reactions["👍"]

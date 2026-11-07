import pytest
"""Tests for comments."""
from bird_mach.collaboration.comments import CommentThread
class TestCommentThread:
    def test_add(self):
        ct = CommentThread()
        c = ct.add("u1", "Hello!")
        assert ct.count == 1
    def test_reply(self):
        ct = CommentThread()
        c = ct.add("u1", "Parent")
        r = ct.add("u2", "Reply", parent_id=c.id)
        replies = ct.get_thread(c.id)
        assert len(replies) == 1
    def test_edit(self):
        ct = CommentThread()
        c = ct.add("u1", "Typo")
        ct.edit(c.id, "Fixed")
        assert ct._comments[c.id].edited


def test_edit_rejects_blank_text():
    from bird_mach.collaboration.comments import CommentThread
    thread = CommentThread()
    c = thread.add("u1", "hello")
    with pytest.raises(ValueError):
        thread.edit(c.id, "   ")
    assert thread.get_thread()[0].text == "hello"

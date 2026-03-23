"""Tests for pagination."""
from bird_mach.api.v2.pagination import paginate_offset, paginate_cursor, encode_cursor, decode_cursor

class TestOffsetPagination:
    def test_first_page(self):
        page = paginate_offset(list(range(50)), offset=0, limit=10)
        assert len(page.items) == 10
        assert page.has_next
        assert not page.has_prev

    def test_last_page(self):
        page = paginate_offset(list(range(25)), offset=20, limit=10)
        assert len(page.items) == 5
        assert not page.has_next

class TestCursorPagination:
    def test_first_page(self):
        page = paginate_cursor(list(range(50)), limit=10)
        assert len(page.items) == 10
        assert page.cursor is not None

    def test_next_page(self):
        items = list(range(50))
        p1 = paginate_cursor(items, limit=10)
        p2 = paginate_cursor(items, after=p1.cursor, limit=10)
        assert p2.items[0] == 11

class TestCursorCodec:
    def test_roundtrip(self):
        data = {"offset": 42}
        assert decode_cursor(encode_cursor(data)) == data

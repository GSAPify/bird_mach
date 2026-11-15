"""Tests for SDK pagination helpers."""
from bird_mach.sdk.pagination import PageIterator, merge_pages


def test_page_iterates_over_items():
    page = PageIterator(items=[1, 2, 3], cursor="c1", has_more=True)
    assert list(page) == [1, 2, 3]

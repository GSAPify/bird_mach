"""Tests for SDK pagination helpers."""
from bird_mach.sdk.pagination import PageIterator, merge_pages


def test_page_iterates_over_items():
    page = PageIterator(items=[1, 2, 3], cursor="c1", has_more=True)
    assert list(page) == [1, 2, 3]


def test_page_length_is_item_count():
    assert len(PageIterator(items=["a", "b"], cursor=None, has_more=False)) == 2


def test_merge_pages_preserves_order():
    pages = [PageIterator([1, 2], "c", True), PageIterator([3], None, False)]
    assert merge_pages(pages) == [1, 2, 3]


def test_merge_pages_handles_empty_input():
    assert merge_pages([]) == []
    assert merge_pages([PageIterator([], None, False)]) == []

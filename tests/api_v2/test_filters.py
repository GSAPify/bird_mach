"""Tests for query filters."""
from bird_mach.api.v2.filters import parse_filters, apply_filters

class TestParseFilters:
    def test_eq(self):
        filters = parse_filters({"name": "test"})
        assert filters[0].operator == "eq"

    def test_operator(self):
        filters = parse_filters({"tempo__gt": "120"})
        assert filters[0].field == "tempo"
        assert filters[0].operator == "gt"

class TestApplyFilters:
    def test_eq_filter(self):
        items = [{"name": "a"}, {"name": "b"}]
        filters = parse_filters({"name": "a"})
        assert len(apply_filters(items, filters)) == 1

    def test_gt_filter(self):
        items = [{"tempo": 100}, {"tempo": 140}]
        filters = parse_filters({"tempo__gt": "120"})
        result = apply_filters(items, filters)
        assert len(result) == 1
        assert result[0]["tempo"] == 140

    def test_contains(self):
        items = [{"title": "Rock Song"}, {"title": "Jazz Night"}]
        filters = parse_filters({"title__contains": "rock"})
        assert len(apply_filters(items, filters)) == 1


def test_eq_does_not_match_missing_field_as_none_string():
    from bird_mach.api.v2.filters import Filter, apply_filters
    items = [{"id": 1, "genre": "rock"}, {"id": 2}]
    assert apply_filters(items, [Filter("genre", "eq", "None")]) == []
    assert apply_filters(items, [Filter("genre", "eq", "rock")]) == [items[0]]


def test_ne_keeps_records_missing_the_field():
    from bird_mach.api.v2.filters import Filter, apply_filters
    items = [{"id": 1, "genre": "rock"}, {"id": 2}]
    assert apply_filters(items, [Filter("genre", "ne", "rock")]) == [items[1]]


def test_in_filter_ignores_records_missing_the_field():
    from bird_mach.api.v2.filters import Filter, apply_filters
    items = [{"id": 1, "genre": "rock"}, {"id": 2}, {"id": 3, "genre": "jazz"}]
    result = apply_filters(items, [Filter("genre", "in", "None,rock")])
    assert result == [items[0]]

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

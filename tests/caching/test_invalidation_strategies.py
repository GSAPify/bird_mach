"""Tests for cache invalidation strategies."""
from bird_mach.caching.strategy_v1 import InvalidationStrategy1
from bird_mach.caching.strategy_v2 import InvalidationStrategy2
from bird_mach.caching.strategy_v3 import InvalidationStrategy3


def test_strategy1_starts_at_zero():
    assert InvalidationStrategy1().count == 0


def test_strategy1_invalidate_counts_calls():
    strategy = InvalidationStrategy1()
    assert strategy.invalidate("a") is True
    assert strategy.invalidate("b") is True
    assert strategy.count == 2

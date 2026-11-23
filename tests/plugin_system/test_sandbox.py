"""Tests for plugin sandbox."""
import time
from bird_mach.plugin_system.sandbox import PluginSandbox
class TestSandbox:
    def test_fast_function(self):
        sb = PluginSandbox(max_time_s=1.0)
        result = sb.execute(lambda: 42)
        assert result == 42
    def test_returns_value(self):
        sb = PluginSandbox()
        result = sb.execute(sum, [1, 2, 3])
        assert result == 6


def test_timeout_is_raised_without_waiting_for_the_plugin():
    import time

    import pytest

    from bird_mach.plugin_system.sandbox import PluginSandbox

    start = time.monotonic()
    with pytest.raises(TimeoutError):
        PluginSandbox(max_time_s=0.1).execute(time.sleep, 1.0)
    assert time.monotonic() - start < 0.6

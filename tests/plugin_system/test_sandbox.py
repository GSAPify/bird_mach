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

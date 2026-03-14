"""Tests for plugin registry."""
from bird_mach.plugin_system.registry import PluginRegistry

class FakePlugin:
    name = "test-plugin"
    version = "1.0.0"
    def activate(self): pass
    def deactivate(self): pass

class TestPluginRegistry:
    def test_register(self):
        reg = PluginRegistry()
        reg.register(FakePlugin())
        assert reg.plugin_count == 1

    def test_activate(self):
        reg = PluginRegistry()
        reg.register(FakePlugin())
        assert reg.activate("test-plugin")
        assert len(reg.get_active()) == 1

    def test_deactivate(self):
        reg = PluginRegistry()
        reg.register(FakePlugin())
        reg.activate("test-plugin")
        reg.deactivate("test-plugin")
        assert len(reg.get_active()) == 0

    def test_hooks(self):
        reg = PluginRegistry()
        results = []
        reg.register_hook("on_frame", lambda **kw: results.append(kw))

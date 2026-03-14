"""Tests for plugin loader."""
from pathlib import Path
from bird_mach.plugin_system.loader import PluginLoader
class TestPluginLoader:
    def test_discover_empty(self, tmp_path):
        loader = PluginLoader(tmp_path)
        assert loader.discover() == []
    def test_discover_finds_plugins(self, tmp_path):
        (tmp_path / "my_plugin.py").write_text("x = 1")
        loader = PluginLoader(tmp_path)
        assert "my_plugin" in loader.discover()
    def test_load(self, tmp_path):
        (tmp_path / "test_plug.py").write_text("VALUE = 42")
        loader = PluginLoader(tmp_path)
        mod = loader.load("test_plug")
        assert mod.VALUE == 42

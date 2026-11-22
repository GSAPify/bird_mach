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


def test_plugin_named_like_stdlib_does_not_replace_it(tmp_path):
    import sys
    import types

    from bird_mach.plugin_system.loader import PluginLoader

    (tmp_path / "types.py").write_text("MARK = 1\n")
    module = PluginLoader(tmp_path).load("types")
    assert module.MARK == 1
    assert sys.modules["types"] is types


def test_failed_plugin_import_leaves_no_module_behind(tmp_path):
    import sys

    import pytest

    from bird_mach.plugin_system.loader import PluginLoader

    (tmp_path / "broken.py").write_text("raise RuntimeError('boom')\n")
    with pytest.raises(RuntimeError):
        PluginLoader(tmp_path).load("broken")
    assert "mach_plugin_broken" not in sys.modules

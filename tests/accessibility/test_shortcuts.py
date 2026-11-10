"""Tests for keyboard shortcuts."""
from bird_mach.accessibility.keyboard_shortcuts import ShortcutRegistry, Shortcut

class TestShortcutRegistry:
    def test_default_shortcuts(self):
        reg = ShortcutRegistry()
        assert reg.get_by_key("Space") is not None

    def test_get_by_category(self):
        reg = ShortcutRegistry()
        playback = reg.get_by_category("playback")
        assert len(playback) >= 5

    def test_add_custom(self):
        reg = ShortcutRegistry()
        reg.add(Shortcut("X", "custom_action", "Do something", "custom"))
        assert reg.get_by_key("X") is not None

    def test_help_text(self):
        reg = ShortcutRegistry()
        text = reg.to_help_text()
        assert "Keyboard Shortcuts" in text
        assert "Space" in text


def test_editing_one_registry_does_not_touch_defaults():
    from bird_mach.accessibility.keyboard_shortcuts import DEFAULT_SHORTCUTS, ShortcutRegistry
    original = next(s.description for s in DEFAULT_SHORTCUTS if s.key == "M")
    ShortcutRegistry().get_by_key("M").description = "changed"
    assert ShortcutRegistry().get_by_key("M").description == original

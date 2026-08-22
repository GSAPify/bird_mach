"""Keyboard shortcut registry and documentation."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Shortcut:
    key: str
    action: str
    description: str
    category: str = "general"

DEFAULT_SHORTCUTS = [
    Shortcut("Space", "toggle_play", "Play / Pause audio", "playback"),
    Shortcut("←", "seek_back", "Seek back 5 seconds", "playback"),
    Shortcut("→", "seek_forward", "Seek forward 5 seconds", "playback"),
    Shortcut("↑", "volume_up", "Increase volume", "playback"),
    Shortcut("↓", "volume_down", "Decrease volume", "playback"),
    Shortcut("M", "toggle_mute", "Mute / Unmute", "playback"),
    Shortcut("F", "toggle_fullscreen", "Toggle fullscreen", "view"),
    Shortcut("2", "view_2d", "Switch to 2D view", "view"),
    Shortcut("3", "view_3d", "Switch to 3D view", "view"),
    Shortcut("L", "toggle_live", "Toggle live mode", "capture"),
    Shortcut("R", "toggle_record", "Start / Stop recording", "capture"),
    Shortcut("?", "show_help", "Show keyboard shortcuts", "general"),
]

class ShortcutRegistry:
    def __init__(self):
        self._shortcuts = list(DEFAULT_SHORTCUTS)

    def add(self, shortcut: Shortcut) -> None:
        if self.get_by_key(shortcut.key) is not None:
            raise ValueError(f"shortcut {shortcut.key!r} is already registered")
        self._shortcuts.append(shortcut)

    def get_by_key(self, key: str) -> Shortcut | None:
        for s in self._shortcuts:
            if s.key == key:
                return s
        return None

    def get_by_category(self, category: str) -> list[Shortcut]:
        return [s for s in self._shortcuts if s.category == category]

    def to_help_text(self) -> str:
        lines = ["Keyboard Shortcuts", "=" * 40]
        cats = {}
        for s in self._shortcuts:
            cats.setdefault(s.category, []).append(s)
        for cat, shortcuts in cats.items():
            lines.append(f"\n## {cat.title()}")
            for s in shortcuts:
                lines.append(f"  {s.key:>8}  {s.description}")
        return "\n".join(lines)

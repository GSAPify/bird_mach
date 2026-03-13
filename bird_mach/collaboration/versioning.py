"""Version control for audio analysis configurations."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import copy

@dataclass
class ConfigVersion:
    version: int
    config: dict
    author: str
    message: str
    created_at: datetime = field(default_factory=datetime.now)

class ConfigVersioning:
    def __init__(self):
        self._versions: list[ConfigVersion] = []

    def commit(self, config: dict, author: str, message: str) -> ConfigVersion:
        v = ConfigVersion(
            version=len(self._versions) + 1,
            config=copy.deepcopy(config),
            author=author, message=message,
        )
        self._versions.append(v)
        return v

    def get(self, version: int) -> ConfigVersion | None:
        if 1 <= version <= len(self._versions):
            return self._versions[version - 1]
        return None

    @property
    def latest(self) -> ConfigVersion | None:
        return self._versions[-1] if self._versions else None

    @property
    def version_count(self) -> int:
        return len(self._versions)

    def diff(self, v1: int, v2: int) -> dict:
        c1 = self.get(v1)
        c2 = self.get(v2)
        if not c1 or not c2:
            return {}
        changes = {}
        all_keys = set(c1.config) | set(c2.config)
        for k in all_keys:
            old = c1.config.get(k)
            new = c2.config.get(k)
            if old != new:
                changes[k] = {"old": old, "new": new}
        return changes

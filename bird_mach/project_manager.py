"""Project management for organizing audio analyses."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AudioProject:
    id: str
    name: str
    owner_id: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    audio_ids: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    is_archived: bool = False

    def add_audio(self, audio_id: str) -> None:
        if audio_id not in self.audio_ids:
            self.audio_ids.append(audio_id)

    def remove_audio(self, audio_id: str) -> None:
        self.audio_ids = [a for a in self.audio_ids if a != audio_id]

class ProjectManager:
    def __init__(self):
        self._projects: dict[str, AudioProject] = {}

    def create(self, name: str, owner_id: str, description: str = "") -> AudioProject:
        if not name or not name.strip():
            raise ValueError("project name must not be empty")
        if not owner_id or not owner_id.strip():
            raise ValueError("owner_id must not be empty")
        project = AudioProject(
            id=str(uuid.uuid4())[:8], name=name,
            owner_id=owner_id, description=description,
        )
        self._projects[project.id] = project
        return project

    def get(self, project_id: str) -> AudioProject | None:
        return self._projects.get(project_id)

    def list_for_user(self, owner_id: str) -> list[AudioProject]:
        return [p for p in self._projects.values()
                if p.owner_id == owner_id and not p.is_archived]

    def archive(self, project_id: str) -> bool:
        p = self._projects.get(project_id)
        if p:
            p.is_archived = True
            return True
        return False

    def delete(self, project_id: str) -> bool:
        return self._projects.pop(project_id, None) is not None

    def search(self, query: str) -> list[AudioProject]:
        q = query.strip().lower()
        if not q:
            return []
        return [p for p in self._projects.values()
                if not p.is_archived
                and (q in p.name.lower() or q in p.description.lower()
                     or any(q in t.lower() for t in p.tags))]

"""RTSP session management for audio streaming."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class RTSPSession:
    session_id: str
    client_ip: str
    transport: str = "RTP/AVP"
    created_at: datetime = field(default_factory=datetime.now)
    is_playing: bool = False
    packets_sent: int = 0

class RTSPServer:
    """Manage RTSP sessions for audio delivery."""
    def __init__(self, port: int = 8554):
        self._port = port
        self._sessions: dict[str, RTSPSession] = {}

    def create_session(self, client_ip: str) -> RTSPSession:
        sid = str(uuid.uuid4())[:8]
        session = RTSPSession(session_id=sid, client_ip=client_ip)
        self._sessions[sid] = session
        return session

    def play(self, session_id: str) -> bool:
        s = self._sessions.get(session_id)
        if s:
            s.is_playing = True
            return True
        return False

    def teardown(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

    @property
    def active_sessions(self) -> int:
        return sum(1 for s in self._sessions.values() if s.is_playing)

    @property
    def total_sessions(self) -> int:
        return len(self._sessions)

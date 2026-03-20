"""Tests for RTSP server."""
from bird_mach.streaming.rtsp import RTSPServer

class TestRTSPServer:
    def test_create_session(self):
        srv = RTSPServer()
        s = srv.create_session("192.168.1.1")
        assert s.client_ip == "192.168.1.1"
        assert srv.total_sessions == 1

    def test_play(self):
        srv = RTSPServer()
        s = srv.create_session("10.0.0.1")
        srv.play(s.session_id)
        assert srv.active_sessions == 1

    def test_teardown(self):
        srv = RTSPServer()
        s = srv.create_session("10.0.0.1")
        assert srv.teardown(s.session_id)
        assert srv.total_sessions == 0

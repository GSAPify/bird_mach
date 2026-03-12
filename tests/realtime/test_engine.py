"""Tests for the real-time audio engine."""
import asyncio
import numpy as np
import pytest
from bird_mach.realtime.engine import RealtimeEngine, AudioFrame, EngineConfig

class TestAudioFrame:
    def test_duration(self):
        frame = AudioFrame(samples=np.zeros(22050), sample_rate=22050, timestamp_ms=0)
        assert abs(frame.duration_ms - 1000.0) < 1

    def test_rms_silence(self):
        frame = AudioFrame(samples=np.zeros(1024), sample_rate=44100, timestamp_ms=0)
        assert frame.rms == 0.0

    def test_rms_signal(self):
        frame = AudioFrame(samples=np.ones(1024) * 0.5, sample_rate=44100, timestamp_ms=0)
        assert frame.rms > 0

class TestEngineConfig:
    def test_defaults(self):
        cfg = EngineConfig()
        assert cfg.buffer_size == 2048
        assert cfg.sample_rate == 44100

class TestRealtimeEngine:
    def test_init(self):
        engine = RealtimeEngine()
        assert not engine.is_running
        assert engine.frames_processed == 0

    @pytest.mark.asyncio
    async def test_start_stop(self):
        engine = RealtimeEngine()
        await engine.start()
        assert engine.is_running
        await engine.stop()
        assert not engine.is_running

    @pytest.mark.asyncio
    async def test_process_frame(self):
        engine = RealtimeEngine()
        frame = AudioFrame(
            samples=np.random.randn(2048).astype(np.float32),
            sample_rate=44100, timestamp_ms=0.0,
        )
        result = await engine.process_frame(frame)
        assert "rms" in result
        assert "peak" in result
        assert "centroid" in result
        assert result["frame_id"] == 1

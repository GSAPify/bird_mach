"""Tests for async SDK client."""
import pytest
from bird_mach.sdk.async_client import AsyncMachClient

class TestAsyncMachClient:
    @pytest.mark.asyncio
    async def test_connect(self):
        c = AsyncMachClient()
        assert await c.connect()

    @pytest.mark.asyncio
    async def test_analyze(self):
        c = AsyncMachClient()
        await c.connect()
        result = await c.analyze("test.wav")
        assert result["status"] == "queued"

    @pytest.mark.asyncio
    async def test_batch(self):
        c = AsyncMachClient()
        await c.connect()
        results = await c.batch_analyze(["a.wav", "b.wav"])
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_disconnected(self):
        c = AsyncMachClient()
        with pytest.raises(ConnectionError):
            await c.analyze("test.wav")

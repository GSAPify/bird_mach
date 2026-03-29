# Mach SDK

## Installation
```bash
pip install mach-sdk
```

## Quick Start
```python
from bird_mach.sdk.client import MachClient
client = MachClient()
client.connect()
result = client.analyze("audio.wav")
```

## Async Usage
```python
from bird_mach.sdk.async_client import AsyncMachClient
async with AsyncMachClient() as client:
    result = await client.analyze("audio.wav")
    batch = await client.batch_analyze(["a.wav", "b.wav"])
```

## Models
- `AnalysisResult` — Complete analysis output
- `SearchResult` — Search hit with score
- `BatchResult` — Batch operation summary

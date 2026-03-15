# Real-Time Audio Engine

## Overview
The real-time engine processes audio frames at low latency for
live visualization, beat detection, and pitch tracking.

## Components
- **RealtimeEngine**: Core processing pipeline
- **RingBuffer**: Circular sample buffer
- **DSP utilities**: FFT bands, windowing, spectral flux
- **WebSocket manager**: Client connection handling
- **Beat tracker**: Real-time BPM estimation
- **Pitch tracker**: Autocorrelation-based f0 detection
- **Loudness meter**: Simplified LUFS metering
- **Session recorder**: Capture live sessions

## Usage
```python
from bird_mach.realtime.engine import RealtimeEngine, AudioFrame
engine = RealtimeEngine()
await engine.start()
result = await engine.process_frame(frame)
```

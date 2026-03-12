# Real-Time API Reference

## Engine
```python
engine = RealtimeEngine(EngineConfig(buffer_size=4096))
await engine.start()
result = await engine.process_frame(frame)
await engine.stop()
```

## DSP
```python
bands = compute_fft_bands(spectrum, sr=44100)
windowed = apply_window(samples, "hann")
fb = mel_filterbank(sr=22050, n_fft=2048, n_mels=40)
```

## WebSocket
```python
mgr = AudioWebSocketManager(max_clients=100)
client = mgr.register("client-1", time.time())
mgr.subscribe("client-1", "audio")
await mgr.broadcast("audio", data)
```

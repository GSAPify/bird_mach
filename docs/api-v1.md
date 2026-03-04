# API v1 Reference

The `/api/v1/` endpoints provide JSON-based programmatic access to Mach's analysis features.

## Endpoints

### `GET /api/v1/health`

Returns service health status.

```json
{"status": "ok", "app": "Mach", "version": "0.4.0"}
```

### `POST /api/v1/analyze`

Upload an audio file and receive a JSON analysis summary.

**Request**: `multipart/form-data` with `file` field.

**Query Parameters**:
- `sr` (int, default 22050): Target sample rate.

**Response**:
```json
{
  "duration_s": 30.5,
  "sample_rate": 22050,
  "tempo_bpm": 128.0,
  "onset_count": 64,
  "rms_mean": 0.12,
  "rms_max": 0.85,
  "spectral_centroid_mean": 2400.5,
  "spectral_bandwidth_mean": 1800.3,
  "zero_crossing_rate_mean": 0.06,
  "tags": ["pop/rock", "bright"]
}
```

## Error Responses

All errors follow this format:
```json
{"status": "error", "error": "description", "detail": "optional details"}
```

## Authentication

No authentication required for local development. For production, add an API key middleware.

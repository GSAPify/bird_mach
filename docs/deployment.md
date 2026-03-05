# Deployment Guide

## Docker

Build and run with Docker:

```bash
docker build -t mach .
docker run -p 8000:8000 mach
```

Or use Docker Compose:

```bash
docker compose up
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_JSON` | `false` | JSON-formatted logs |
| `MAX_UPLOAD_MB` | `50` | Max file upload size |
| `MAX_AUDIO_DURATION_S` | `600` | Max audio duration |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins |
| `WORKERS` | `1` | Uvicorn worker count |

## Health Check

```bash
curl http://localhost:8000/health
```

## Production Tips

- Set `WORKERS` to 2-4x CPU cores for multi-process serving
- Use a reverse proxy (nginx/Caddy) for TLS termination
- Set `CORS_ORIGINS` to your frontend domain
- Enable `LOG_JSON=true` for structured log aggregation

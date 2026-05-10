# Deployment Guide

## Docker

Build and run with Docker:

```bash
docker build -t mach .
docker run -p 8000:8000 mach
```

The image honors the platform-provided `PORT` variable, defaulting to `8000`
when it is not set.

Or use Docker Compose:

```bash
docker compose up
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Runtime environment label exposed by `/health` |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_JSON` | `false` | JSON-formatted logs |
| `MAX_UPLOAD_MB` | `50` | Max file upload size |
| `MAX_AUDIO_DURATION_S` | `600` | Max audio duration |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins |
| `WORKERS` | `1` | Uvicorn worker count |
| `RENDER_EXTERNAL_URL` | empty | Public Render URL shown in the footer when configured |

## Health Check

```bash
curl http://localhost:8000/health
```

## Render Free Plan

The repository includes a `render.yaml` Blueprint:

```yaml
services:
  - type: web
    name: bird-mach
    runtime: docker
    plan: free
    autoDeployTrigger: commit
    healthCheckPath: /health
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: LOG_LEVEL
        value: INFO
      - key: MAX_UPLOAD_MB
        value: "50"
```

To deploy it, connect the GitHub repository to Render and create a new
Blueprint from the repo. Render provides HTTPS, which is required by browser
microphone and tab-audio capture outside `localhost`.

After Render marks the service live, point the smoke check at the public URL:

```bash
BASE_URL=https://your-render-service.onrender.com make smoke
```

For ongoing operations, see the [Render runbook](runbooks/render.md).

## Production Tips

- Set `WORKERS` to 2-4x CPU cores for multi-process serving
- Use a reverse proxy (nginx/Caddy) for TLS termination
- Set `CORS_ORIGINS` to your frontend domain
- Enable `LOG_JSON=true` for structured log aggregation

# Render Runbook

## Purpose

Use this checklist when the Mach web app is live on Render and needs a quick
production sanity check after a push.

## Smoke Check

```bash
BASE_URL=https://your-render-service.onrender.com make smoke
```

Expected result: `scripts/health_check.sh` exits successfully after receiving a
2xx response from `/health`.

## Manual Checks

- Open `/` and confirm the upload form, static CSS, and static JS load.
- Open `/live` over HTTPS and confirm the browser shows mic and tab-audio
  controls.
- Open `/health` and confirm `status`, `service`, `version`, `environment`, and
  `max_upload_mb` are present.
- Uploads larger than `MAX_UPLOAD_MB` should fail before audio processing.

## Rollback

Render can redeploy any previous commit from the service activity page. After a
rollback, rerun the smoke check and open `/health` to confirm the version that is
serving traffic.

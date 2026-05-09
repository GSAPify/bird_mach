#!/bin/bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
curl -sf "${BASE_URL%/}/health" >/dev/null

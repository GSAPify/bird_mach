#!/bin/bash
curl -sf http://localhost:8000/health || exit 1

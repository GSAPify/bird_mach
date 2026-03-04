"""Standardized API response helpers."""

from __future__ import annotations

from typing import Any

from fastapi.responses import JSONResponse


def success(data: Any, *, status_code: int = 200) -> JSONResponse:
    return JSONResponse(content={"status": "ok", "data": data}, status_code=status_code)


def error(message: str, *, status_code: int = 400, detail: str = "") -> JSONResponse:
    body = {"status": "error", "error": message}
    if detail:
        body["detail"] = detail
    return JSONResponse(content=body, status_code=status_code)

"""API endpoint for tracing."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/tracing", tags=["tracing"])

    @router.get("/")
    async def list_tracing(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_tracing(item_id: str):
        return {"id": item_id, "type": "tracing"}

    @router.post("/")
    async def create_tracing(data: dict):
        return {"id": "new", "type": "tracing", **data}

    @router.put("/{item_id}")
    async def update_tracing(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_tracing(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for metrics."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/metrics", tags=["metrics"])

    @router.get("/")
    async def list_metrics(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_metrics(item_id: str):
        return {"id": item_id, "type": "metrics"}

    @router.post("/")
    async def create_metrics(data: dict):
        return {"id": "new", "type": "metrics", **data}

    @router.put("/{item_id}")
    async def update_metrics(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_metrics(item_id: str):
        return {"id": item_id, "deleted": True}

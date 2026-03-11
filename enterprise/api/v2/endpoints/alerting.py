"""API endpoint for alerting."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/alerting", tags=["alerting"])

    @router.get("/")
    async def list_alerting(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_alerting(item_id: str):
        return {"id": item_id, "type": "alerting"}

    @router.post("/")
    async def create_alerting(data: dict):
        return {"id": "new", "type": "alerting", **data}

    @router.put("/{item_id}")
    async def update_alerting(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_alerting(item_id: str):
        return {"id": item_id, "deleted": True}

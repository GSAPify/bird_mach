"""API endpoint for notifications."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/notifications", tags=["notifications"])

    @router.get("/")
    async def list_notifications(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_notifications(item_id: str):
        return {"id": item_id, "type": "notifications"}

    @router.post("/")
    async def create_notifications(data: dict):
        return {"id": "new", "type": "notifications", **data}

    @router.put("/{item_id}")
    async def update_notifications(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_notifications(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for usage_metering."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/usage_metering", tags=["usage_metering"])

    @router.get("/")
    async def list_usage_metering(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_usage_metering(item_id: str):
        return {"id": item_id, "type": "usage_metering"}

    @router.post("/")
    async def create_usage_metering(data: dict):
        return {"id": "new", "type": "usage_metering", **data}

    @router.put("/{item_id}")
    async def update_usage_metering(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_usage_metering(item_id: str):
        return {"id": item_id, "deleted": True}

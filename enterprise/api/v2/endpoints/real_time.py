"""API endpoint for real_time."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/real_time", tags=["real_time"])

    @router.get("/")
    async def list_real_time(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_real_time(item_id: str):
        return {"id": item_id, "type": "real_time"}

    @router.post("/")
    async def create_real_time(data: dict):
        return {"id": "new", "type": "real_time", **data}

    @router.put("/{item_id}")
    async def update_real_time(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_real_time(item_id: str):
        return {"id": item_id, "deleted": True}

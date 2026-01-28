"""API endpoint for filtering."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/filtering", tags=["filtering"])

    @router.get("/")
    async def list_filtering(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_filtering(item_id: str):
        return {"id": item_id, "type": "filtering"}

    @router.post("/")
    async def create_filtering(data: dict):
        return {"id": "new", "type": "filtering", **data}

    @router.put("/{item_id}")
    async def update_filtering(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_filtering(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for caching."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/caching", tags=["caching"])

    @router.get("/")
    async def list_caching(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_caching(item_id: str):
        return {"id": item_id, "type": "caching"}

    @router.post("/")
    async def create_caching(data: dict):
        return {"id": "new", "type": "caching", **data}

    @router.put("/{item_id}")
    async def update_caching(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_caching(item_id: str):
        return {"id": item_id, "deleted": True}

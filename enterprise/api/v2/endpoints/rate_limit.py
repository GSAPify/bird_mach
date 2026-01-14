"""API endpoint for rate_limit."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/rate_limit", tags=["rate_limit"])

    @router.get("/")
    async def list_rate_limit(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_rate_limit(item_id: str):
        return {"id": item_id, "type": "rate_limit"}

    @router.post("/")
    async def create_rate_limit(data: dict):
        return {"id": "new", "type": "rate_limit", **data}

    @router.put("/{item_id}")
    async def update_rate_limit(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_rate_limit(item_id: str):
        return {"id": item_id, "deleted": True}

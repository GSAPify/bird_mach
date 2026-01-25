"""API endpoint for sse."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/sse", tags=["sse"])

    @router.get("/")
    async def list_sse(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_sse(item_id: str):
        return {"id": item_id, "type": "sse"}

    @router.post("/")
    async def create_sse(data: dict):
        return {"id": "new", "type": "sse", **data}

    @router.put("/{item_id}")
    async def update_sse(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_sse(item_id: str):
        return {"id": item_id, "deleted": True}

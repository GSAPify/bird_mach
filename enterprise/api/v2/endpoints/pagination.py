"""API endpoint for pagination."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/pagination", tags=["pagination"])

    @router.get("/")
    async def list_pagination(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_pagination(item_id: str):
        return {"id": item_id, "type": "pagination"}

    @router.post("/")
    async def create_pagination(data: dict):
        return {"id": "new", "type": "pagination", **data}

    @router.put("/{item_id}")
    async def update_pagination(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_pagination(item_id: str):
        return {"id": item_id, "deleted": True}

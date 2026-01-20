"""API endpoint for search."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/search", tags=["search"])

    @router.get("/")
    async def list_search(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_search(item_id: str):
        return {"id": item_id, "type": "search"}

    @router.post("/")
    async def create_search(data: dict):
        return {"id": "new", "type": "search", **data}

    @router.put("/{item_id}")
    async def update_search(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_search(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for api_keys."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/api_keys", tags=["api_keys"])

    @router.get("/")
    async def list_api_keys(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_api_keys(item_id: str):
        return {"id": item_id, "type": "api_keys"}

    @router.post("/")
    async def create_api_keys(data: dict):
        return {"id": "new", "type": "api_keys", **data}

    @router.put("/{item_id}")
    async def update_api_keys(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_api_keys(item_id: str):
        return {"id": item_id, "deleted": True}

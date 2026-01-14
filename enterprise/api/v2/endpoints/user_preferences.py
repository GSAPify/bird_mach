"""API endpoint for user_preferences."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/user_preferences", tags=["user_preferences"])

    @router.get("/")
    async def list_user_preferences(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_user_preferences(item_id: str):
        return {"id": item_id, "type": "user_preferences"}

    @router.post("/")
    async def create_user_preferences(data: dict):
        return {"id": "new", "type": "user_preferences", **data}

    @router.put("/{item_id}")
    async def update_user_preferences(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_user_preferences(item_id: str):
        return {"id": item_id, "deleted": True}

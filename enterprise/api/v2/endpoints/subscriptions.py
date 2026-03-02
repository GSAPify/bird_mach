"""API endpoint for subscriptions."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

    @router.get("/")
    async def list_subscriptions(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_subscriptions(item_id: str):
        return {"id": item_id, "type": "subscriptions"}

    @router.post("/")
    async def create_subscriptions(data: dict):
        return {"id": "new", "type": "subscriptions", **data}

    @router.put("/{item_id}")
    async def update_subscriptions(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_subscriptions(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for sms."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/sms", tags=["sms"])

    @router.get("/")
    async def list_sms(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_sms(item_id: str):
        return {"id": item_id, "type": "sms"}

    @router.post("/")
    async def create_sms(data: dict):
        return {"id": "new", "type": "sms", **data}

    @router.put("/{item_id}")
    async def update_sms(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_sms(item_id: str):
        return {"id": item_id, "deleted": True}

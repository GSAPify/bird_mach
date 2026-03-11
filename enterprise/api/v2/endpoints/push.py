"""API endpoint for push."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/push", tags=["push"])

    @router.get("/")
    async def list_push(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_push(item_id: str):
        return {"id": item_id, "type": "push"}

    @router.post("/")
    async def create_push(data: dict):
        return {"id": "new", "type": "push", **data}

    @router.put("/{item_id}")
    async def update_push(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_push(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for email."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/email", tags=["email"])

    @router.get("/")
    async def list_email(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_email(item_id: str):
        return {"id": item_id, "type": "email"}

    @router.post("/")
    async def create_email(data: dict):
        return {"id": "new", "type": "email", **data}

    @router.put("/{item_id}")
    async def update_email(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_email(item_id: str):
        return {"id": item_id, "deleted": True}

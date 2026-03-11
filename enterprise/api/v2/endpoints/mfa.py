"""API endpoint for mfa."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/mfa", tags=["mfa"])

    @router.get("/")
    async def list_mfa(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_mfa(item_id: str):
        return {"id": item_id, "type": "mfa"}

    @router.post("/")
    async def create_mfa(data: dict):
        return {"id": "new", "type": "mfa", **data}

    @router.put("/{item_id}")
    async def update_mfa(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_mfa(item_id: str):
        return {"id": item_id, "deleted": True}

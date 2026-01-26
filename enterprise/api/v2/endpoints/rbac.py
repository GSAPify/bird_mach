"""API endpoint for rbac."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/rbac", tags=["rbac"])

    @router.get("/")
    async def list_rbac(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_rbac(item_id: str):
        return {"id": item_id, "type": "rbac"}

    @router.post("/")
    async def create_rbac(data: dict):
        return {"id": "new", "type": "rbac", **data}

    @router.put("/{item_id}")
    async def update_rbac(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_rbac(item_id: str):
        return {"id": item_id, "deleted": True}

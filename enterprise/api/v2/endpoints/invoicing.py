"""API endpoint for invoicing."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/invoicing", tags=["invoicing"])

    @router.get("/")
    async def list_invoicing(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_invoicing(item_id: str):
        return {"id": item_id, "type": "invoicing"}

    @router.post("/")
    async def create_invoicing(data: dict):
        return {"id": "new", "type": "invoicing", **data}

    @router.put("/{item_id}")
    async def update_invoicing(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_invoicing(item_id: str):
        return {"id": item_id, "deleted": True}

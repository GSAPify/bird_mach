"""API endpoint for billing."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/billing", tags=["billing"])

    @router.get("/")
    async def list_billing(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_billing(item_id: str):
        return {"id": item_id, "type": "billing"}

    @router.post("/")
    async def create_billing(data: dict):
        return {"id": "new", "type": "billing", **data}

    @router.put("/{item_id}")
    async def update_billing(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_billing(item_id: str):
        return {"id": item_id, "deleted": True}

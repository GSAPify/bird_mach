"""API endpoint for data_export."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/data_export", tags=["data_export"])

    @router.get("/")
    async def list_data_export(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_data_export(item_id: str):
        return {"id": item_id, "type": "data_export"}

    @router.post("/")
    async def create_data_export(data: dict):
        return {"id": "new", "type": "data_export", **data}

    @router.put("/{item_id}")
    async def update_data_export(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_data_export(item_id: str):
        return {"id": item_id, "deleted": True}

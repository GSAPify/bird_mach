"""API endpoint for dashboard."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/dashboard", tags=["dashboard"])

    @router.get("/")
    async def list_dashboard(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_dashboard(item_id: str):
        return {"id": item_id, "type": "dashboard"}

    @router.post("/")
    async def create_dashboard(data: dict):
        return {"id": "new", "type": "dashboard", **data}

    @router.put("/{item_id}")
    async def update_dashboard(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_dashboard(item_id: str):
        return {"id": item_id, "deleted": True}

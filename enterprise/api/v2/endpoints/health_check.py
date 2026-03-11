"""API endpoint for health_check."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/health_check", tags=["health_check"])

    @router.get("/")
    async def list_health_check(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_health_check(item_id: str):
        return {"id": item_id, "type": "health_check"}

    @router.post("/")
    async def create_health_check(data: dict):
        return {"id": "new", "type": "health_check", **data}

    @router.put("/{item_id}")
    async def update_health_check(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_health_check(item_id: str):
        return {"id": item_id, "deleted": True}

"""API endpoint for long_polling."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/long_polling", tags=["long_polling"])

    @router.get("/")
    async def list_long_polling(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_long_polling(item_id: str):
        return {"id": item_id, "type": "long_polling"}

    @router.post("/")
    async def create_long_polling(data: dict):
        return {"id": "new", "type": "long_polling", **data}

    @router.put("/{item_id}")
    async def update_long_polling(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_long_polling(item_id: str):
        return {"id": item_id, "deleted": True}

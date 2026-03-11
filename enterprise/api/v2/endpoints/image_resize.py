"""API endpoint for image_resize."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/image_resize", tags=["image_resize"])

    @router.get("/")
    async def list_image_resize(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_image_resize(item_id: str):
        return {"id": item_id, "type": "image_resize"}

    @router.post("/")
    async def create_image_resize(data: dict):
        return {"id": "new", "type": "image_resize", **data}

    @router.put("/{item_id}")
    async def update_image_resize(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_image_resize(item_id: str):
        return {"id": item_id, "deleted": True}

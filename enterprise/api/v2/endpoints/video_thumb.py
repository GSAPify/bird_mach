"""API endpoint for video_thumb."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/video_thumb", tags=["video_thumb"])

    @router.get("/")
    async def list_video_thumb(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_video_thumb(item_id: str):
        return {"id": item_id, "type": "video_thumb"}

    @router.post("/")
    async def create_video_thumb(data: dict):
        return {"id": "new", "type": "video_thumb", **data}

    @router.put("/{item_id}")
    async def update_video_thumb(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_video_thumb(item_id: str):
        return {"id": item_id, "deleted": True}

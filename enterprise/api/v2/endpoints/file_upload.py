"""API endpoint for file_upload."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/file_upload", tags=["file_upload"])

    @router.get("/")
    async def list_file_upload(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_file_upload(item_id: str):
        return {"id": item_id, "type": "file_upload"}

    @router.post("/")
    async def create_file_upload(data: dict):
        return {"id": "new", "type": "file_upload", **data}

    @router.put("/{item_id}")
    async def update_file_upload(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_file_upload(item_id: str):
        return {"id": item_id, "deleted": True}

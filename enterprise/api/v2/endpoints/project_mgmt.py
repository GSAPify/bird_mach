"""API endpoint for project_mgmt."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/project_mgmt", tags=["project_mgmt"])

    @router.get("/")
    async def list_project_mgmt(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_project_mgmt(item_id: str):
        return {"id": item_id, "type": "project_mgmt"}

    @router.post("/")
    async def create_project_mgmt(data: dict):
        return {"id": "new", "type": "project_mgmt", **data}

    @router.put("/{item_id}")
    async def update_project_mgmt(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_project_mgmt(item_id: str):
        return {"id": item_id, "deleted": True}

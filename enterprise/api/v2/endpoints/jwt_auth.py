"""API endpoint for jwt_auth."""
    from __future__ import annotations
    from fastapi import APIRouter, Depends, HTTPException
    router = APIRouter(prefix="/jwt_auth", tags=["jwt_auth"])

    @router.get("/")
    async def list_jwt_auth(skip: int = 0, limit: int = 20):
        return {"items": [], "total": 0, "skip": skip, "limit": limit}

    @router.get("/{item_id}")
    async def get_jwt_auth(item_id: str):
        return {"id": item_id, "type": "jwt_auth"}

    @router.post("/")
    async def create_jwt_auth(data: dict):
        return {"id": "new", "type": "jwt_auth", **data}

    @router.put("/{item_id}")
    async def update_jwt_auth(item_id: str, data: dict):
        return {"id": item_id, "updated": True}

    @router.delete("/{item_id}")
    async def delete_jwt_auth(item_id: str):
        return {"id": item_id, "deleted": True}

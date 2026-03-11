"""rbac serializers."""

def serialize_rbac(obj) -> dict:
    return {"type": "rbac", "data": str(obj)}

def deserialize_rbac(data: dict):
    return data.get("data")

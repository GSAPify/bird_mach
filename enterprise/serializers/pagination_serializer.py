"""pagination serializers."""

def serialize_pagination(obj) -> dict:
    return {"type": "pagination", "data": str(obj)}

def deserialize_pagination(data: dict):
    return data.get("data")

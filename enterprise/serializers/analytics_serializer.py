"""analytics serializers."""

def serialize_analytics(obj) -> dict:
    return {"type": "analytics", "data": str(obj)}

def deserialize_analytics(data: dict):
    return data.get("data")

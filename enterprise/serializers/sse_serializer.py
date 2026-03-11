"""sse serializers."""

def serialize_sse(obj) -> dict:
    return {"type": "sse", "data": str(obj)}

def deserialize_sse(data: dict):
    return data.get("data")

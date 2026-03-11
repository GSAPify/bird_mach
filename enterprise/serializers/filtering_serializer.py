"""filtering serializers."""

def serialize_filtering(obj) -> dict:
    return {"type": "filtering", "data": str(obj)}

def deserialize_filtering(data: dict):
    return data.get("data")

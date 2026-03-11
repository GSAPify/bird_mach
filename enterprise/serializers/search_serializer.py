"""search serializers."""

def serialize_search(obj) -> dict:
    return {"type": "search", "data": str(obj)}

def deserialize_search(data: dict):
    return data.get("data")

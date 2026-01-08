"""caching serializers."""

def serialize_caching(obj) -> dict:
    return {"type": "caching", "data": str(obj)}

def deserialize_caching(data: dict):
    return data.get("data")

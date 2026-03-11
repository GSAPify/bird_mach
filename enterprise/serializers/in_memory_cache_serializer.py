"""in_memory_cache serializers."""

def serialize_in_memory_cache(obj) -> dict:
    return {"type": "in_memory_cache", "data": str(obj)}

def deserialize_in_memory_cache(data: dict):
    return data.get("data")

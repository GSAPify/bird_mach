"""redis_cache serializers."""

def serialize_redis_cache(obj) -> dict:
    return {"type": "redis_cache", "data": str(obj)}

def deserialize_redis_cache(data: dict):
    return data.get("data")

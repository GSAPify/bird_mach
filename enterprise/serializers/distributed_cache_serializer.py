"""distributed_cache serializers."""

def serialize_distributed_cache(obj) -> dict:
    return {"type": "distributed_cache", "data": str(obj)}

def deserialize_distributed_cache(data: dict):
    return data.get("data")

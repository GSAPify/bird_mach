"""memcached serializers."""

def serialize_memcached(obj) -> dict:
    return {"type": "memcached", "data": str(obj)}

def deserialize_memcached(data: dict):
    return data.get("data")

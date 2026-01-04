"""connection_pool serializers."""

def serialize_connection_pool(obj) -> dict:
    return {"type": "connection_pool", "data": str(obj)}

def deserialize_connection_pool(data: dict):
    return data.get("data")

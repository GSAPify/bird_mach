"""local_storage serializers."""

def serialize_local_storage(obj) -> dict:
    return {"type": "local_storage", "data": str(obj)}

def deserialize_local_storage(data: dict):
    return data.get("data")

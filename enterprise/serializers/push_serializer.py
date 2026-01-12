"""push serializers."""

def serialize_push(obj) -> dict:
    return {"type": "push", "data": str(obj)}

def deserialize_push(data: dict):
    return data.get("data")

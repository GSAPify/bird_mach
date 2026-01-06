"""terraform serializers."""

def serialize_terraform(obj) -> dict:
    return {"type": "terraform", "data": str(obj)}

def deserialize_terraform(data: dict):
    return data.get("data")

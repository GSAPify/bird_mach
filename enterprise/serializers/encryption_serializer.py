"""encryption serializers."""

def serialize_encryption(obj) -> dict:
    return {"type": "encryption", "data": str(obj)}

def deserialize_encryption(data: dict):
    return data.get("data")

"""mfa serializers."""

def serialize_mfa(obj) -> dict:
    return {"type": "mfa", "data": str(obj)}

def deserialize_mfa(data: dict):
    return data.get("data")

"""email serializers."""

def serialize_email(obj) -> dict:
    return {"type": "email", "data": str(obj)}

def deserialize_email(data: dict):
    return data.get("data")

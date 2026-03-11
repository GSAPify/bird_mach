"""oauth2 serializers."""

def serialize_oauth2(obj) -> dict:
    return {"type": "oauth2", "data": str(obj)}

def deserialize_oauth2(data: dict):
    return data.get("data")

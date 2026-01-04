"""api_keys serializers."""

def serialize_api_keys(obj) -> dict:
    return {"type": "api_keys", "data": str(obj)}

def deserialize_api_keys(data: dict):
    return data.get("data")

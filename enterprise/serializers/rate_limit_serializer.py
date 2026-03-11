"""rate_limit serializers."""

def serialize_rate_limit(obj) -> dict:
    return {"type": "rate_limit", "data": str(obj)}

def deserialize_rate_limit(data: dict):
    return data.get("data")

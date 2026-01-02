"""health_check serializers."""

def serialize_health_check(obj) -> dict:
    return {"type": "health_check", "data": str(obj)}

def deserialize_health_check(data: dict):
    return data.get("data")

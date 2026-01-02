"""logging serializers."""

def serialize_logging(obj) -> dict:
    return {"type": "logging", "data": str(obj)}

def deserialize_logging(data: dict):
    return data.get("data")

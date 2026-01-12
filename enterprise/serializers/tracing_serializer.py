"""tracing serializers."""

def serialize_tracing(obj) -> dict:
    return {"type": "tracing", "data": str(obj)}

def deserialize_tracing(data: dict):
    return data.get("data")

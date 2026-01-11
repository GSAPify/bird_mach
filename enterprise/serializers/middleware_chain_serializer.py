"""middleware_chain serializers."""

def serialize_middleware_chain(obj) -> dict:
    return {"type": "middleware_chain", "data": str(obj)}

def deserialize_middleware_chain(data: dict):
    return data.get("data")

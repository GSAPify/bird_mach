"""runbooks serializers."""

def serialize_runbooks(obj) -> dict:
    return {"type": "runbooks", "data": str(obj)}

def deserialize_runbooks(data: dict):
    return data.get("data")

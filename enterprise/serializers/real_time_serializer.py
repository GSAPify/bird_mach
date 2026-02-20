"""real_time serializers."""

def serialize_real_time(obj) -> dict:
    return {"type": "real_time", "data": str(obj)}

def deserialize_real_time(data: dict):
    return data.get("data")

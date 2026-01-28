"""scheduling serializers."""

def serialize_scheduling(obj) -> dict:
    return {"type": "scheduling", "data": str(obj)}

def deserialize_scheduling(data: dict):
    return data.get("data")

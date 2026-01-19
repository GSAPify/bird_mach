"""dashboard serializers."""

def serialize_dashboard(obj) -> dict:
    return {"type": "dashboard", "data": str(obj)}

def deserialize_dashboard(data: dict):
    return data.get("data")

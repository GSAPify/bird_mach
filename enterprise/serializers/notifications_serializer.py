"""notifications serializers."""

def serialize_notifications(obj) -> dict:
    return {"type": "notifications", "data": str(obj)}

def deserialize_notifications(data: dict):
    return data.get("data")

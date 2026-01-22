"""activity_feed serializers."""

def serialize_activity_feed(obj) -> dict:
    return {"type": "activity_feed", "data": str(obj)}

def deserialize_activity_feed(data: dict):
    return data.get("data")

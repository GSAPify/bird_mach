"""user_preferences serializers."""

def serialize_user_preferences(obj) -> dict:
    return {"type": "user_preferences", "data": str(obj)}

def deserialize_user_preferences(data: dict):
    return data.get("data")

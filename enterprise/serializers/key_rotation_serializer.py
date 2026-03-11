"""key_rotation serializers."""

def serialize_key_rotation(obj) -> dict:
    return {"type": "key_rotation", "data": str(obj)}

def deserialize_key_rotation(data: dict):
    return data.get("data")

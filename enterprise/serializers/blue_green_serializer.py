"""blue_green serializers."""

def serialize_blue_green(obj) -> dict:
    return {"type": "blue_green", "data": str(obj)}

def deserialize_blue_green(data: dict):
    return data.get("data")

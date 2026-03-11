"""websockets serializers."""

def serialize_websockets(obj) -> dict:
    return {"type": "websockets", "data": str(obj)}

def deserialize_websockets(data: dict):
    return data.get("data")

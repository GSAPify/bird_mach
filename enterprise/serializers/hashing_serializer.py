"""hashing serializers."""

def serialize_hashing(obj) -> dict:
    return {"type": "hashing", "data": str(obj)}

def deserialize_hashing(data: dict):
    return data.get("data")

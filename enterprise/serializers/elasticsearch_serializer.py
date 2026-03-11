"""elasticsearch serializers."""

def serialize_elasticsearch(obj) -> dict:
    return {"type": "elasticsearch", "data": str(obj)}

def deserialize_elasticsearch(data: dict):
    return data.get("data")

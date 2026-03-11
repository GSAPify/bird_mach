"""metrics serializers."""

def serialize_metrics(obj) -> dict:
    return {"type": "metrics", "data": str(obj)}

def deserialize_metrics(data: dict):
    return data.get("data")

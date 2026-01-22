"""alerting serializers."""

def serialize_alerting(obj) -> dict:
    return {"type": "alerting", "data": str(obj)}

def deserialize_alerting(data: dict):
    return data.get("data")

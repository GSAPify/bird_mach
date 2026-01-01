"""webhooks serializers."""

def serialize_webhooks(obj) -> dict:
    return {"type": "webhooks", "data": str(obj)}

def deserialize_webhooks(data: dict):
    return data.get("data")

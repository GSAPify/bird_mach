"""sms serializers."""

def serialize_sms(obj) -> dict:
    return {"type": "sms", "data": str(obj)}

def deserialize_sms(data: dict):
    return data.get("data")

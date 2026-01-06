"""usage_metering serializers."""

def serialize_usage_metering(obj) -> dict:
    return {"type": "usage_metering", "data": str(obj)}

def deserialize_usage_metering(data: dict):
    return data.get("data")

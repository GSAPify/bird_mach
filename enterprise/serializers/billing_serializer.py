"""billing serializers."""

def serialize_billing(obj) -> dict:
    return {"type": "billing", "data": str(obj)}

def deserialize_billing(data: dict):
    return data.get("data")

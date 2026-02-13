"""invoicing serializers."""

def serialize_invoicing(obj) -> dict:
    return {"type": "invoicing", "data": str(obj)}

def deserialize_invoicing(data: dict):
    return data.get("data")

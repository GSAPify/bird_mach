"""currency serializers."""

def serialize_currency(obj) -> dict:
    return {"type": "currency", "data": str(obj)}

def deserialize_currency(data: dict):
    return data.get("data")

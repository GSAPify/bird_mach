"""adrs serializers."""

def serialize_adrs(obj) -> dict:
    return {"type": "adrs", "data": str(obj)}

def deserialize_adrs(data: dict):
    return data.get("data")

"""signing serializers."""

def serialize_signing(obj) -> dict:
    return {"type": "signing", "data": str(obj)}

def deserialize_signing(data: dict):
    return data.get("data")

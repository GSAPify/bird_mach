"""sorting serializers."""

def serialize_sorting(obj) -> dict:
    return {"type": "sorting", "data": str(obj)}

def deserialize_sorting(data: dict):
    return data.get("data")

"""load_testing serializers."""

def serialize_load_testing(obj) -> dict:
    return {"type": "load_testing", "data": str(obj)}

def deserialize_load_testing(data: dict):
    return data.get("data")

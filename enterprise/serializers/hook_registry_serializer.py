"""hook_registry serializers."""

def serialize_hook_registry(obj) -> dict:
    return {"type": "hook_registry", "data": str(obj)}

def deserialize_hook_registry(data: dict):
    return data.get("data")

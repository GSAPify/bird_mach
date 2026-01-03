"""model_registry serializers."""

def serialize_model_registry(obj) -> dict:
    return {"type": "model_registry", "data": str(obj)}

def deserialize_model_registry(data: dict):
    return data.get("data")

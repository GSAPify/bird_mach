"""ml_inference serializers."""

def serialize_ml_inference(obj) -> dict:
    return {"type": "ml_inference", "data": str(obj)}

def deserialize_ml_inference(data: dict):
    return data.get("data")

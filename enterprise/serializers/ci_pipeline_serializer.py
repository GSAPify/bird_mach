"""ci_pipeline serializers."""

def serialize_ci_pipeline(obj) -> dict:
    return {"type": "ci_pipeline", "data": str(obj)}

def deserialize_ci_pipeline(data: dict):
    return data.get("data")

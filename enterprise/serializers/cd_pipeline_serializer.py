"""cd_pipeline serializers."""

def serialize_cd_pipeline(obj) -> dict:
    return {"type": "cd_pipeline", "data": str(obj)}

def deserialize_cd_pipeline(data: dict):
    return data.get("data")
